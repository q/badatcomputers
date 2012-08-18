from django.conf.urls import patterns, include, url

## Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # django-registration
    (r'^accounts/', include('registration.urls')),

    # Examples:
    url(r'^$', 'gungnir.core.views.index', name='gungnir_index'),
    #    url(r'^derp/', include('gungnir.derp.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
