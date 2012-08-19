from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404

from gungnir.projects.models import Application, Repo
from gungnir.projects.forms import ApplicationForm, RepoForm
from gungnir.projects.tasks import pre_fetch_repo

from gungnir.builds.models import Build, BuildConfig
from gungnir.builds.forms import BuildForm, BuildConfigForm

from djcelery.views import task_view


# Wrapper to our celery task
pre_fetch_repo_view = task_view(pre_fetch_repo)

class ApplicationDetailView(DetailView):
    model = Application
#    template_name = 'projects/app_list.html'

#    def get_context_data(self, **kwargs):
#        context = super(ApplicationDetailView, self).get_context_data(**kwargs)
#        return context

class ApplicationCreate(CreateView):
    model = Application
    form_class = ApplicationForm
    success_url=reverse_lazy('gungnir-core-dashboard')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(ApplicationCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ApplicationCreate, self).get_context_data(**kwargs)
        context['page_title'] = 'Create Application'
        context['page_header'] = 'Create Application'
        context['form_submit_text'] = 'Create'
        return context

class RepoDetailView(DetailView):
    model = Repo

class RepoCreate(CreateView):
    model = Repo
    form_class = RepoForm
    success_url=reverse_lazy('gungnir-core-dashboard')

    def get_form(self, form_class):
        form = super(RepoCreate,self).get_form(form_class)
        form.fields['application'].queryset = Application.objects.filter(owner=self.request.user)
        return form

    def form_valid(self, form):
        form.instance.application.owner = self.request.user
        return super(RepoCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(RepoCreate, self).get_context_data(**kwargs)
        context['page_title'] = 'Link Repo'
        context['page_header'] = 'Link Repo'
        context['form_submit_text'] = 'Link'
        return context
        
class RepoUpdate(UpdateView):
    model = Repo
    form_class = RepoForm
    success_url=reverse_lazy('gungnir-core-dashboard')
    
    def get_object(self, queryset=None):
        obj = Repo.objects.get(id=self.kwargs['id'])
        return obj
    
    def get_form(self, form_class):
        form = super(RepoUpdate,self).get_form(form_class)
        form.fields['application'].queryset = Application.objects.filter(owner=self.request.user)
        return form

    def form_valid(self, form):
        form.instance.application.owner = self.request.user
        return super(RepoUpdate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(RepoUpdate, self).get_context_data(**kwargs)
        context['page_title'] = 'Update Repo'
        context['page_header'] = 'Update Repo'
        context['form_submit_text'] = 'Update'
        return context

class BuildDetailView(DetailView):
    model = Build

class BuildCreate(CreateView):
    model = Build
    form_class = BuildForm
    success_url=reverse_lazy('gungnir-core-dashboard')

    def get_form(self, form_class):
        form = super(BuildCreate,self).get_form(form_class)
        form.fields['application'].queryset = Application.objects.filter(owner=self.request.user)
        return form

    def form_valid(self, form):
        form.instance.application.owner = self.request.user
        messages.add_message(self.request, messages.INFO, 'Build is now in process. This can take up to 5 minutes.')
        return super(BuildCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(BuildCreate, self).get_context_data(**kwargs)
        context['page_title'] = 'Link Build'
        context['page_header'] = 'Link Build'
        context['form_submit_text'] = 'Link'
        return context
        
class BuildUpdate(UpdateView):
    model = Build
    form_class = BuildForm
    success_url=reverse_lazy('gungnir-core-dashboard')
    
    def get_object(self, queryset=None):
        obj = Build.objects.get(id=self.kwargs['id'])
        return obj

    def get_form(self, form_class):
        form = super(BuildUpdate,self).get_form(form_class)
        form.fields['application'].queryset = Application.objects.filter(owner=self.request.user)
        return form

    def form_valid(self, form):
        form.instance.application.owner = self.request.user
        return super(BuildUpdate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(BuildUpdate, self).get_context_data(**kwargs)
        context['page_title'] = 'Update Build'
        context['page_header'] = 'Update Build'
        context['form_submit_text'] = 'Update'
        return context

class BuildConfigDetailView(DetailView):
    model = BuildConfig
 
class BuildConfigCreate(CreateView):
    model = BuildConfig
    form_class = BuildConfigForm
    success_url=reverse_lazy('gungnir-core-dashboard')

    def get_form(self, form_class):
        form = super(BuildConfigCreate,self).get_form(form_class)
        form.fields['application'].queryset = Application.objects.filter(owner=self.request.user)
        return form

    def form_valid(self, form):
        form.instance.application.owner = self.request.user
        return super(BuildConfigCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(BuildConfigCreate, self).get_context_data(**kwargs)
        context['page_title'] = 'Link BuildConfig'
        context['page_header'] = 'Link BuildConfig'
        context['form_submit_text'] = 'Link'
        return context

class BuildConfigUpdate(UpdateView):
    model = BuildConfig
    form_class = BuildConfigForm
    success_url=reverse_lazy('gungnir-core-dashboard')
    
    def get_object(self, queryset=None):
        obj = BuildConfig.objects.get(id=self.kwargs['id'])
        return obj

    def get_form(self, form_class):
        form = super(BuildConfigUpdate,self).get_form(form_class)
        form.fields['application'].queryset = Application.objects.filter(owner=self.request.user)
        return form

    def form_valid(self, form):
        form.instance.application.owner = self.request.user
        return super(BuildConfigUpdate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(BuildConfigCreate, self).get_context_data(**kwargs)
        context['page_title'] = 'Update BuildConfig'
        context['page_header'] = 'Update BuildConfig'
        context['form_submit_text'] = 'Update'
        return context  
