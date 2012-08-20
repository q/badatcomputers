from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import TemplateView, ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from gungnir.core.forms import ProfileForm
from gungnir.projects.models import Application, Repo

def index(request):
    return render_to_response('core/base.html', {}, context_instance=RequestContext(request))


class ProfileView(TemplateView):
    template_name = "core/profile.html"
    
    @method_decorator(login_required)
    def get(self, request):
        profile = request.user.get_profile()
        
        form = ProfileForm({
            'aws_akey':profile.aws_akey,
            'aws_skey':profile.aws_skey,
        })
        return self.render_to_response({'form':form})
    
    @method_decorator(login_required)
    def post(self, request):
        form = ProfileForm(request.POST, request.FILES)
        profile = request.user.get_profile()
        
        if form.is_valid():
            profile.aws_akey=form.cleaned_data['aws_akey']
            profile.aws_skey=form.cleaned_data['aws_skey']
            profile.save()
        
        form = ProfileForm({
            'aws_akey':profile.aws_akey,
            'aws_skey':profile.aws_skey,
        })
        return self.render_to_response({'form':form})

class DashboardView(TemplateView):
    template_name =  "core/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        context['app_list'] = Application.objects.filter(owner=self.request.user)
        return context

class DashboardListView(ListView):
    model = Application
    template_name =  "core/dashboard.html"

    def get_queryset(self):
        qs = Application.objects.filter(owner=self.request.user)
        return qs
