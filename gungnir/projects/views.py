from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
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

    def dispatch(self, *args, **kwargs):
        self.app = get_object_or_404(Application, pk=kwargs.get('pk'))
        return super(RepoCreate, self).dispatch(*args, **kwargs)

#    def get_form(self, form_class):
#        form = super(RepoCreate,self).get_form(form_class)
#        #form.fields['application'].queryset = Application.objects.filter(owner=self.request.user)
#        return form

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.application = self.app
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

#    def form_valid(self, form):
#        #form.instance.application.owner = self.request.user
#        return super(RepoCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(RepoCreate, self).get_context_data(**kwargs)
        context['page_title'] = 'Link Repo'
        context['page_header'] = 'Link Repo to {0}'.format(self.app.name)
        context['form_submit_text'] = 'Link'
        return context
        
class RepoUpdate(UpdateView):
    model = Repo
    form_class = RepoForm
    success_url=reverse_lazy('gungnir-core-dashboard')
    
    def get_object(self, queryset=None):
        obj = Repo.objects.get(id=self.kwargs['pk'])
        return obj
    
#    def get_form(self, form_class):
#        form = super(RepoUpdate,self).get_form(form_class)
#        #form.fields['application'].queryset = Application.objects.filter(owner=self.request.user)
#        return form

#    def form_valid(self, form):
#        form.instance.application.owner = self.request.user
#        return super(RepoUpdate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(RepoUpdate, self).get_context_data(**kwargs)
        context['page_title'] = 'Update Repo'
        context['page_header'] = 'Update Repo'
        context['form_submit_text'] = 'Update'
        return context
        
class RepoDelete(DeleteView):
    model = Repo
    success_url=reverse_lazy('gungnir-core-dashboard')
    
    def get_object(self, queryset=None):
        obj = Repo.objects.get(id=self.kwargs['pk'])
        return obj

class BuildDetailView(DetailView):
    model = Build

class BuildCreate(CreateView):
    model = Build
    form_class = BuildForm
    success_url=reverse_lazy('gungnir-core-dashboard')

    def dispatch(self, *args, **kwargs):
        self.app = get_object_or_404(Application, pk=kwargs.get('pk'))
        return super(BuildCreate, self).dispatch(*args, **kwargs)

    def get_form(self, form_class):
        form = super(BuildCreate,self).get_form(form_class)
        form.fields['config'].queryset = BuildConfig.objects.filter(application=self.app)
        return form

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.application = self.app
        self.object.save()
        messages.add_message(self.request, messages.INFO, 'Build is now in process. This can take up to 5 minutes. IN DJANGODASH TESTING THESE WILL GET DELETED AFTER HALF AN HOUR.')
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(BuildCreate, self).get_context_data(**kwargs)
        context['page_title'] = 'Create Build'
        context['page_header'] = 'Create Build for {0}'.format(self.app.name)
        context['form_submit_text'] = 'Build'
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

class BuildDelete(DeleteView):
    model = Repo
    success_url=reverse_lazy('gungnir-core-dashboard')
    
    def get_object(self, queryset=None):
        obj = Build.objects.get(id=self.kwargs['pk'])
        return obj

class BuildConfigDetailView(DetailView):
    model = BuildConfig
 
class BuildConfigCreate(CreateView):
    model = BuildConfig
    form_class = BuildConfigForm
    success_url=reverse_lazy('gungnir-core-dashboard')

    def dispatch(self, *args, **kwargs):
        self.app = get_object_or_404(Application, pk=kwargs.get('pk'))
        return super(BuildConfigCreate, self).dispatch(*args, **kwargs)

    def get_form(self, form_class):
        form = super(BuildConfigCreate,self).get_form(form_class)
        form.fields['repo'].queryset = Repo.objects.filter(application=self.app)
        return form

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.application = self.app
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(BuildConfigCreate, self).get_context_data(**kwargs)
        context['page_title'] = 'Add BuildConfig'
        context['page_header'] = 'Add BuildConfig to {0}'.format(self.app.name)
        context['form_submit_text'] = 'Add'
        return context

class BuildConfigUpdate(UpdateView):
    model = BuildConfig
    form_class = BuildConfigForm
    success_url=reverse_lazy('gungnir-core-dashboard')

#    def dispatch(self, *args, **kwargs):
#        self.app = get_object_or_404(Application, pk=kwargs.get('pk'))
#        return super(BuildConfigUpdate, self).dispatch(*args, **kwargs)

    def get_object(self, queryset=None):
        obj = BuildConfig.objects.get(id=self.kwargs['pk'], application__owner=self.request.user)
        return obj

    def get_form(self, form_class):
        form = super(BuildConfigUpdate,self).get_form(form_class)
        form.fields['repo'].queryset = Repo.objects.filter(application=self.object.application)
        return form

    def get_context_data(self, **kwargs):
        context = super(BuildConfigUpdate, self).get_context_data(**kwargs)
        context['page_title'] = 'Update BuildConfig'
        context['page_header'] = 'Update BuildConfig'
        context['form_submit_text'] = 'Update'
        return context  

class BuildConfigDelete(DeleteView):
    model = Repo
    success_url=reverse_lazy('gungnir-core-dashboard')
    
    def get_object(self, queryset=None):
        obj = BuildConfig.objects.get(id=self.kwargs['pk'])
        return obj