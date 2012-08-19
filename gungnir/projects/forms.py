from django.forms import ModelForm
from gungnir.projects.models import Repo

""" 
ModelForms 
"""
class RepoForm(ModelForm):
    class Meta:
        model = Repo