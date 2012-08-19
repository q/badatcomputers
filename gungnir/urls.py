from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from core.forms import CompatEmailUserCreationForm
from emailusernames.forms import EmailAuthenticationForm

from builds.views import *

from projects.views import *

urlpatterns = patterns('',
    # Examples:
    #    url(r'^derp/', include('gungnir.derp.urls')),
    url(r'^', include('gungnir.core.urls')),

    url(r'^admin/', include(admin.site.urls)),

    # celery task views
    url(r'^tasks/builds/build_image/(?P<build_config_id>\d+)$', build_image_view),

    # generic views
    (r'^AwsBaseAmi/$',AwsBaseAmiView.as_view()),
    (r'^BuildConfig/$',BuildConfigView.as_view()),
    (r'^Build/$',BuildView.as_view()),
    (r'^SupervisordCommand/$',SupervisordCommandView.as_view()),
    (r'^PythonRequirements/$',PythonRequirementsView.as_view()),
    (r'^Repo/$',RepoView.as_view()),
    
    # django-celery
    url(r'^celery/', include('djcelery.urls')),
    
    # django-registration - this is retarded how they suggest you override these. fact, you should just not include these urls...
    url(r'^accounts/register/$',
        'registration.views.register',
        {
            'backend': 'registration.backends.default.DefaultBackend',
            'form_class': CompatEmailUserCreationForm,
        },
        name='registration_register'),
    url(r'^accounts/login/$',
        'django.contrib.auth.views.login',
        {'authentication_form': EmailAuthenticationForm,},
        name='auth_login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='auth_logout'),
    # this has to be last, so stupid.
    (r'^accounts/', include('registration.backends.default.urls')),
)
