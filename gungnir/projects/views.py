from django.views.generic import TemplateView, DetailView
from django.views.generic.edit import CreateView

from django.shortcuts import get_object_or_404

from gungnir.projects.models import Application
from gungnir.projects.forms import ApplicationForm, RepoForm

class RepoView(TemplateView):
    template_name = "projects/repo.html"
    
    def get(self, request):
        return self.render_to_response({'form':RepoForm})

class ApplicationDetailView(DetailView):
    model = Application
#    template_name = 'projects/app_list.html'

#    def get_context_data(self, **kwargs):
#        context = super(ApplicationDetailView, self).get_context_data(**kwargs)
#        return context


class ApplicationCreate(CreateView):
        model = Application
        form_class = ApplicationForm

        def form_valid(self, form):
            form.instance.owner = self.request.user
            return super(ApplicationCreate, self).form_valid(form)

        def get_context_data(self, **kwargs):
            context = super(ApplicationCreate, self).get_context_data(**kwargs)
            context['page_title'] = 'Create Application'
            context['page_header'] = 'Create Application'
            context['form_submit_text'] = 'Create'
            return context

#class AuthorDetailView(DetailView):
#
#    queryset = Author.objects.all()
#
#    def get_object(self):
#        # Call the superclass
#        object = super(AuthorDetailView, self).get_object()
#        # Record the last accessed date
#        object.last_accessed = timezone.now()
#        object.save()
#        # Return the object
#        return object