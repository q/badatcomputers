from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import TemplateView
from gungnir.core.forms import ProfileForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

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
        if form.is_valid():
            profile = request.user.get_profile()
            
            profile.aws_akey=form.cleaned_data['aws_akey']
            profile.aws_skey=form.cleaned_data['aws_skey']
            profile.save()
            print profile.aws_akey
        
        form = ProfileForm({
            'aws_akey':profile.aws_akey,
            'aws_skey':profile.aws_skey,
        })
        return self.render_to_response({'form':form})