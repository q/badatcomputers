from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView, RedirectView
from django.contrib.auth.decorators import login_required

from gungnir.core.views import ProfileView, DashboardView, DashboardListView

urlpatterns = patterns('gungnir.core.views',
    url(r'^$', RedirectView.as_view(url=reverse_lazy('gungnir-core-about')), name='gungnir-core-index'),
    url(r'^about/$', TemplateView.as_view(template_name='core/about.html'), name='gungnir-core-about'),
    url(r'^profile/$', login_required(ProfileView.as_view()), name='profile'),
    url(r'^dashboard/$', login_required(DashboardView.as_view()), name='gungnir-core-dashboard'),
    url(r'^dashboard2/$', login_required(DashboardListView.as_view()), name='gungnir-core-dashboard2'),

)