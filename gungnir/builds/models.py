from django.db import models
from gungnir.core.models import BaseModel

OS_CHOICES = (
    (0, 'ubuntu'),
    (1, 'centos'),
    )

class AwsBaseAmi(BaseModel):
    AMI_REGION_CHOICES = (
        (0, 'us-east-1'),
        (1, 'us-west-1'),
    )
    AMI_ARCH_CHOICES = (
        (0, 'i386'),
        (1, 'amd64'),
    )
    AMI_STORAGE_CHOICES = (
        (0, 'ebs'),
        (1, 'instance-store'),
    )

    region = models.PositiveSmallIntegerField(choices=AMI_REGION_CHOICES, default=0)
    arch = models.PositiveSmallIntegerField(choices=AMI_ARCH_CHOICES, default=1)
    storage = models.PositiveSmallIntegerField(choices=AMI_STORAGE_CHOICES, default=0)
    ami_id = models.CharField(max_length=15)
    aki_id = models.CharField(max_length=15, blank=True)
    description = models.TextField(blank=True)

class BuildConfig(BaseModel):
    WEBSERVER_CHOICES = (
        (0, 'apache'),
        (1, 'gunicorn'),
    )
    BUILD_TYPE_CHOICES = (
        (0, 'Deploy'),
        (1, 'AWS AMI'),
    )

    parent_config = models.ForeignKey('self')
    application = models.ForeignKey('projects.Application')
    repo = models.ForeignKey('projects.Repo')

    os = models.PositiveSmallIntegerField(choices=OS_CHOICES, default=1)
    webserver = models.PositiveSmallIntegerField(choices=WEBSERVER_CHOICES, default=1)
    build_type = models.PositiveIntegerField(choices=BUILD_TYPE_CHOICES, default=1)

    requirements = models.ManyToManyField('PythonRequirements')
    use_virtualenv = models.BooleanField(default=False) # dont use for now...
    deploy_root	 = models.CharField(max_length='256', default='/opt/venvs') # Location venvs will reside

    # django specific
    static_root = models.CharField(max_length=256, blank=True) # Location of static root, None value will result in no files being served from the AMI
    media_root = models.CharField(max_length=256, blank=True) # Location of media root, None value will result in no files being served from the AMI

    # aws specific
    aws_base_ami = models.ForeignKey(AwsBaseAmi)
    aws_keypair_name = models.CharField(max_length=32) # no idea how long these can be
    aws_ami_public = models.BooleanField(default=True)  # Set this to make the AMIs produced public

class Build(BaseModel):
    """
    once we've built an ami from a config, put it here...
    """
    config = models.ForeignKey(BuildConfig)
    ami_id = models.CharField(max_length=15)
    code_version = models.CharField(max_length=10, blank=True)

#class Deploy()

class SupervisordCommand(BaseModel):
    build_config = models.ForeignKey(BuildConfig)
    name = models.CharField(max_length=255)
    cmd = models.CharField(max_length=255)  # Templated command name for example '/{deploy_root}/bin/manage.py' will fill in deploy_root from AMI
    directory = models.CharField(default='{PROJECT_ROOT}', max_length=255) # Directory to work out of
    user = models.CharField(default='root', max_length=64) # User to run the supd command as

class PythonRequirements(BaseModel):
    config = models.ManyToManyField('BuildConfig')
    os = models.PositiveSmallIntegerField(choices=OS_CHOICES, default=1)
    pypi_name = models.CharField(max_length=128) # Actual python package name that you would pass to pip
    os_package = models.CharField(max_length=128) # Required OS package for the package name
    build_only = models.BooleanField(default=False) # Indicate whether the package can be removed after AMI build
