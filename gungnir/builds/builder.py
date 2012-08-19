from fabric.api import env, sudo, run, output, cd
from fabric.operations import put
from fabric.network import NetworkError
import os
import boto
from django.conf import settings
from django.template.loader import render_to_string

from datetime import datetime

import time

CONNECTABLE_INSTANCE_STATES = ['running']

def wait_for_instance(instance):
    poll_interval = 30

    print 'Instance state is: ', instance.update()
    instance_state =  instance.state

    if not instance_state in CONNECTABLE_INSTANCE_STATES:
        print 'Instance not ready...sleeping'
        time.sleep(poll_interval)
        wait_for_instance(instance)

    else:
        return instance


def setup_fab_output():
    output.aborts = True
    output.warnings = True

    output.user = False
    output.stdout = False
    output.stderr = False
    output.running = False
    output.debug = False
    output.status = False

def connect_to_instance(instance, user, key_file):
    wait_for_instance(instance)

    host_string = '{user}@{host}:{port}'.format(user=user, host=instance.public_dns_name, port=22)
    env.host_string = host_string

    if instance.public_dns_name not in env.hosts:
        env.hosts.append(instance.public_dns_name)

    env.key_filename = key_file

    env.warn_only = True
    env.disable_known_hosts = True

    return host_string

from functools import wraps

def builder_fab(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        build_instance = args[0].instance
        #setup_fab_output()
        connect_to_instance(build_instance, args[0].user, args[0].key_file)
        try:
            return func(*args, **kwargs)
        except NetworkError:
            # AWS is lying and the instance probably isnt up yet...sleep a few seconds
            time.sleep(30)
            return func(*args, **kwargs)

    return wrapper

class AwsGunicornUbuntu(object):
    """Class responsible for building AWS instances"""
    required_packages = ['build-essential', 'nginx', 'python-pip', 'python-virtualenv', 'python-dev']

    packages_to_remove = ['build-essential', 'python-dev',]
    required_python_packages = ['supervisor']


    key_file = '/tmp/djangodash2012.pem'
    user = 'ubuntu'

    # Supervisord templates
    supd_conf_template = 'configs/supervisord/supervisord.conf'
    supd_init_template = 'configs/supervisord/supervisord-init'


    # NGINX templates
    nginx_conf_template = 'configs/nginx/app.conf'

    def __init__(self, buildconfig):
        self.is_deployed = False
        self.project = buildconfig
        self.repo = buildconfig.repo

        self.local_app_path = '/tmp/test-app' + '/*'

        self.venv_root = buildconfig.deploy_root
        self.project_name = buildconfig.application.name
        self.project_site_root = self.venv_root + '/' + self.project_name + '/site/'
        self.project_root = self.project_site_root + '/' + self.project_name
        self.project_media_root = buildconfig.media_root
        self.project_static_root = buildconfig.static_root

        self.project_settings = buildconfig.django_settings

        self.requirements_path = 'requirements.txt' #buildconfig.requirements

        self.instance = None
        self.build_config = buildconfig
        self.ec2 = boto.connect_ec2(settings.ACCESS_KEY_ID, settings.SECRET_ACCESS_KEY)
        self.reservation = None
        self.instance_running = False

    def launch_instance(self):
        image = self.ec2.get_image('ami-d99e37b0')
        self.reservation = image.run(key_name='djangodash2012',
            instance_type = 'm1.small',
        )

        self.instance = self.reservation.instances[0]

    @builder_fab
    def install_required_packages(self):
        sudo('apt-get update')
        apt_install_cmd = 'apt-get -y install ' + ' '.join(self.required_packages)
        return sudo(apt_install_cmd)

    @builder_fab
    def build_venv(self):

        # Ensure our venv root directory exists
        sudo('mkdir -p {0}'.format(self.venv_root))

        # Make our virtualenv
        virtual_env_path = os.path.join(self.venv_root, self.project_name)

        sudo('virtualenv {0}'.format(virtual_env_path))

        # Make etc and logs directory
        etc_dir = os.path.join(virtual_env_path, 'etc')
        sudo('mkdir -p {0}'.format(etc_dir))

        logs_dir = os.path.join(virtual_env_path, 'logs')
        sudo('mkdir -p {0}'.format(logs_dir))

        # Make site directory
        sudo('mkdir -p {0}'.format(self.project_root))

        self.fix_permissions(virtual_env_path)

    @builder_fab
    def place_app(self):
        put(self.local_app_path, self.project_root)
        self.fix_permissions(self.project_root)

    @builder_fab
    def install_requirements(self):
        venv_dir  = os.path.join(self.venv_root, self.project_name)
        bin_dir = os.path.join(venv_dir, 'bin')

        full_requirements_path = os.path.join(self.project_root, self.requirements_path)
        pip_cmd = '{bin}/pip install -r {requirements}'.format(bin=bin_dir, requirements=full_requirements_path)
        run(pip_cmd)

        for package in self.required_python_packages:
            pip_cmd = '{bin}/pip install {req}'.format(bin=bin_dir, req=package)
            run(pip_cmd)

    @builder_fab
    def fix_permissions(self, path):
        sudo('chown -R {user} {path}'.format(user=self.user, path=path))


    def _get_template_context(self):
        context = dict()
        context['project_name'] = self.project_name
        context['project_settings'] = self.project_settings
        context['project_root'] = self.project_root
        context['venv_root'] = self.venv_root
        context['commands'] = None
        context['project_static_root'] = self.project_static_root
        context['project_media_root'] = self.project_media_root

        return context

    def _host_string(self):
        return '{user}@{host}:22'.format(user=self.user, host=self.instance.public_dns_name)

    def _push_config(self, config_string, path):
        from fabric.state import connections

        ssh = connections[self._host_string()]

        sftp = ssh.open_sftp()

        remote_file = sftp.open(path, 'rw+')
        remote_file.write(config_string)
        remote_file.close()



    @builder_fab
    def configure_supervisord(self):
        context = self._get_template_context()
        supd_conf = render_to_string(self.supd_conf_template, context)

        supd_init = render_to_string(self.supd_init_template, context)

        venv_path = os.path.join(self.venv_root, self.project_name)
        etc_path = os.path.join(venv_path, 'etc')
        bin_path = os.path.join(venv_path, 'bin')

        supd_conf_path = os.path.join(etc_path, 'supervisord.conf')
        self._push_config(supd_conf, supd_conf_path)
        run('chmod 644 {0}'.format(supd_conf_path))

        supd_init_path = os.path.join(bin_path, '{0}-supervisord'.format(self.project_name))
        self._push_config(supd_init, supd_init_path)
        run('chmod 755 {0}'.format(supd_init_path))


        sudo('ln -s {0} /etc/init.d/{1}-supervisord'.format(supd_init_path, self.project_name))
        sudo('ln -s {0} /etc/rc3.d/S99{1}-supervisord'.format(supd_init_path, self.project_name))

    @builder_fab
    def configure_nginx(self):
        context = self._get_template_context()
        nginx_conf = render_to_string(self.nginx_conf_template, context)

        nginx_conf_dir = '/etc/nginx/sites-available/'
        nginx_conf_fname = self.project_name + '.conf'
        nginx_conf_path = os.path.join(nginx_conf_dir, nginx_conf_fname )


        tmp_nginx_conf = os.path.join('/tmp', nginx_conf_fname)

        self._push_config(nginx_conf, tmp_nginx_conf)

        sudo('rm /etc/nginx/sites-enabled/default')
        sudo('mv {tmp_config} {perm_config}'.format(tmp_config=tmp_nginx_conf, perm_config=nginx_conf_path))
        sudo('ln -s {0} /etc/nginx/sites-enabled/{1}'.format(nginx_conf_path, nginx_conf_fname))
        sudo('service nginx restart')


    @builder_fab
    def remove_unwanted_packages(self):
        apt_cmd = 'apt-get -y remove ' + ' '.join(self.packages_to_remove)

    def deploy(self):
        self.launch_instance()
        self.install_required_packages()
        self.build_venv()
        self.place_app()
        self.install_requirements()
        self.configure_supervisord()
        self.configure_nginx()

        self.is_deployed = True

    def build(self, stop_instance=False):
        if not self.is_deployed:
            self.deploy()

        if stop_instance:
            self.instance.stop()

        image_name = self.project_name + '-' + datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        description = 'Image created by gungnir for {0}'.format(self.build_config.application.name)
        self.ec2.create_image(self.instance.id, image_name, description, no_reboot=False)


