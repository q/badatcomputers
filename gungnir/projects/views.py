from django.views.generic import TemplateView
from gungnir.projects.forms import *

""" 
ModelForms 
"""
class RepoView(TemplateView):
    template_name = "core/Repo.html"
    
    def get(self, request):
        return self.render_to_response({'form':RepoForm})
