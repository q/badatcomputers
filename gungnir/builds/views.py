from django.views.generic import TemplateView
from gungnir.builds.forms import *

class AwsBaseAmiView(TemplateView):
    template_name = "core/AwsBaseAmi.html"
    
    def get(self, request):
        return self.render_to_response({'form':AwsBaseAmiForm})
    
class BuildConfigView(TemplateView):
    template_name = "core/BuildConfig.html"
    
    def get(self, request):
        return self.render_to_response({'form':BuildConfigForm})
    
class BuildView(TemplateView):
    template_name = "core/Build.html"
    
    def get(self, request):
        return self.render_to_response({'form':BuildForm})
    
class SupervisordCommandView(TemplateView):
    template_name = "core/SupervisordCommand.html"
    
    def get(self, request):
        return self.render_to_response({'form':SupervisordCommandForm})
    
class PythonRequirementsView(TemplateView):
    template_name = "core/PythonRequirements.html"
    
    def get(self, request):
        return self.render_to_response({'form':PythonRequirementsForm})