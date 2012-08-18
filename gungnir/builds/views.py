from django.views.generic import TemplateView

class AwsBaseAmiView(TemplateView):
    template_name = "core/AwsBaseAmi.html"
    
class BuildConfigView(TemplateView):
    template_name = "core/BuildConfig.html"
    
class BuildView(TemplateView):
    template_name = "core/Build.html"
    
class SupervisordCommandView(TemplateView):
    template_name = "core/SupervisordCommand.html"
    
class PythonRequirementsView(TemplateView):
    template_name = "core/PythonRequirements.html"