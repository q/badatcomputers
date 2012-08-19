from django.forms import ModelForm
from gungnir.projects.models import Application, Repo

class RepoForm(ModelForm):
    class Meta:
        model = Repo

class ApplicationForm(ModelForm):
    class Meta:
        model = Application
        exclude = ('owner',)
