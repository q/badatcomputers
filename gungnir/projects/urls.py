from django.conf.urls import patterns, url
from django.views.generic import TemplateView, RedirectView
from django.contrib.auth.decorators import login_required

from gungnir.projects.views import ApplicationDetailView, ApplicationCreate, RepoCreate, RepoUpdate, RepoDetailView, pre_fetch_repo_view, BuildCreate, BuildUpdate, BuildConfigCreate, BuildConfigUpdate
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
    url(r'^repo/update/(?P<id>\d+)/$',
        login_required(RepoUpdate.as_view()),
        name='gungnir-projects-repo-update'),
    url(r'^repo/(?P<pk>\d+)/$',
        login_required(RepoDetailView.as_view()),
        name='gungnir-projects-repo-detail'),
    
    url(r'^build/add/$',
        login_required(BuildCreate.as_view()),
        name='gungnir-projects-build-create'),
    url(r'^build/update/(?P<id>\d+)/$',
        login_required(BuildUpdate.as_view()),
        name='gungnir-projects-build-update'),
        
    url(r'^buildconfig/add/$',
        login_required(BuildConfigCreate.as_view()),
        name='gungnir-projects-buildconfig-create'),
    url(r'^buildconfig/update/(?P<id>\d+)/$',
        login_required(BuildConfigUpdate.as_view()),
        name='gungnir-projects-buildconfig-update'),
    
    url(r'^tasks/pre_fetch_repo$', login_required(pre_fetch_repo_view)),

    #    url(r'^$', RedirectView.as_view(url=reverse_lazy('gungnir-core-about')), name='gungnir-core-index'),
#    url(r'^about/$', TemplateView.as_view(template_name='core/about.html'), name='gungnir-core-about'),
#    url(r'^profile/$', login_required(ProfileView.as_view()), name='profile'),
#    url(r'^dashboard/$', login_required(DashboardView.as_view()), name='gungnir-core-dashboard'),
)