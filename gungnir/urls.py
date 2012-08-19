from django.conf.urls import patterns, include, url

## Uncomment the next two lines to enable the admin:
from django.contrib import admin
from core.forms import CompatEmailUserCreationForm
from emailusernames.forms import EmailAuthenticationForm
from builds.views import *
from projects.views import *
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    #    url(r'^derp/', include('gungnir.derp.urls')),
    url(r'^', include('gungnir.core.urls')),

    url(r'^admin/', include(admin.site.urls)),
    
    # generic views
    (r'^AwsBaseAmi/$',AwsBaseAmiView.as_view()),
    (r'^BuildConfig/$',BuildConfigView.as_view()),
    (r'^Build/$',BuildView.as_view()),
    (r'^SupervisordCommand/$',SupervisordCommandView.as_view()),
    (r'^PythonRequirements/$',PythonRequirementsView.as_view()),
    (r'^Repo/$',RepoView.as_view()),
    
    # django-celery
    url(r'^djcelery/', include('djcelery.urls')),
    
    # django-registration
    url(r'^accounts/register/$',
        'registration.views.register',
        {
            'backend': 'registration.backends.default.DefaultBackend',
            'form_class': CompatEmailUserCreationForm,
        },
        name='registration_register'),
    url(r'^accounts/login/$',
        'django.contrib.auth.views.login',
        {
            'authentication_form': EmailAuthenticationForm,
        },
        name='registration_register'),
    (r'^accounts/', include('registration.urls')),
)
