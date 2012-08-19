from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView, DetailView
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required

from django.shortcuts import get_object_or_404

from gungnir.projects.models import Application, Repo
from gungnir.projects.forms import ApplicationForm, RepoForm

from djcelery.views import task_view

# Wrapper to our celery task
pre_fetch_repo_view = login_required(task_view(pre_fetch_repo))

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