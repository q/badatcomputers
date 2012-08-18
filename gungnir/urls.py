from django.conf.urls import patterns, include, url

## Uncomment the next two lines to enable the admin:
from django.contrib import admin
from core.forms import CompatEmailUserCreationForm
from emailusernames.forms import EmailAuthenticationForm
admin.autodiscover()

urlpatterns = patterns('',
    # django-registration
    url(r'^accounts/register/$',
        'registration.views.register',
        {'backend': 'registration.backends.default.DefaultBackend',
        'form_class': CompatEmailUserCreationForm, 
        },
        name='registration_register'),
    url(r'^accounts/login/$',
        'django.contrib.auth.views.login',
        {'authentication_form': EmailAuthenticationForm, 
        },
        name='registration_register'),
    (r'^accounts/', include('registration.urls')),

    # Examples:
    url(r'^$', 'gungnir.core.views.index', name='gungnir_index'),
    #    url(r'^derp/', include('gungnir.derp.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
