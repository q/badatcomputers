from django.conf.urls import patterns, url
from django.views.generic import TemplateView, RedirectView
from django.contrib.auth.decorators import login_required

from gungnir.projects.views import ApplicationDetailView, ApplicationCreate, RepoCreate, RepoDetailView
#from gungnir.core.views import ProfileView, DashboardView


urlpatterns = patterns('gungnir.projects.views',
    url(r'^application/add/$',
        login_required(ApplicationCreate.as_view()),
        name='gungnir-projects-application-create'),
    url(r'^application/(?P<pk>\d+)/$',
        login_required(ApplicationDetailView.as_view()),
        name='gungnir-projects-application-detail'),
    url(r'^repo/add/$',
        login_required(RepoCreate.as_view()),
        name='gungnir-projects-repo-create'),
    url(r'^repo/(?P<pk>\d+)/$',
        login_required(RepoDetailView.as_view()),
        name='gungnir-projects-repo-detail'),


    #    url(r'^$', RedirectView.as_view(url=reverse_lazy('gungnir-core-about')), name='gungnir-core-index'),
#    url(r'^about/$', TemplateView.as_view(template_name='core/about.html'), name='gungnir-core-about'),
#    url(r'^profile/$', login_required(ProfileView.as_view()), name='profile'),
#    url(r'^dashboard/$', login_required(DashboardView.as_view()), name='gungnir-core-dashboard'),
)