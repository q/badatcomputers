PROJECT_NAME = 'gungnir'
PROJECT_ROOT = '/opt/venvs/gungnir/bin/site/badatcomputers'
PROJECT_SETTINGS = 'gungnir.prod_settings'

VENV_PYTHON = '/opt/venvs/gungnir/bin/python'

from fabric.api import run, sudo

def restart_gunicorn():
    sudo('/opt/venvs/gungnir/bin/supervisorctl -c /opt/venvs/gungnir/etc/supervisord.conf restart gungnir-gunicorn')

def git_update():

    with cd(PROJECT_ROOT):
        run('git pull' )
        run('{python} {project_root}/manage.py collectstatic --settings={settings}'.format(python=VENV_PYTHON, project_root=PROJECT_ROOT, settings=PROJECT_SETTINGS ))

def deploy():
    git_update()
    restart_gunicorn()