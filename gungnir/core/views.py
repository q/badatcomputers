from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import TemplateView
from gungnir.core.forms import ProfileForm

def index(request):
    return render_to_response('core/base.html', {}, context_instance=RequestContext(request))
    
class ProfileView(TemplateView):
    template_name = "core/profile.html"
    
    def get(self, request):
        return self.render_to_response({'form':ProfileForm})

class DashboardView(TemplateView):
    template_name =  "core/dashboard.html"