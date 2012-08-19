from django.forms import ModelForm
from gungnir.builds.models import *

class AwsBaseAmiForm(ModelForm):
    class Meta:
        model = AwsBaseAmi

class BuildConfigForm(ModelForm):
    class Meta:
        model = BuildConfig
        exclude = ('parent_config', 'application')

class BuildForm(ModelForm):
    class Meta:
        model = Build
        exclude = ('application', 'ami_id', 'instance_id', 'deploy_status', 'build_date')

class SupervisordCommandForm(ModelForm):
    class Meta:
        model = SupervisordCommand
        
class PythonRequirementsForm(ModelForm):
    class Meta:
        model = PythonRequirements