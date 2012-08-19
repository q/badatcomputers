from django.forms import ModelForm
from gungnir.builds.models import *

""" 
ModelForms 
"""
class AwsBaseAmiForm(ModelForm):
    class Meta:
        model = AwsBaseAmi

class BuildConfigForm(ModelForm):
    class Meta:
        model = BuildConfig
        
class BuildForm(ModelForm):
    class Meta:
        model = Build
        
class SupervisordCommandForm(ModelForm):
    class Meta:
        model = SupervisordCommand
        
class PythonRequirementsForm(ModelForm):
    class Meta:
        model = PythonRequirements