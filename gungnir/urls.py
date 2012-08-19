from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from core.forms import CompatEmailUserCreationForm, CoreEmailAuthForm
#from emailusernames.forms import EmailAuthenticationForm

from builds.views import *

from projects.views import *

urlpatterns = patterns('',
    url(r'^', include('gungnir.core.urls')),
    url(r'^projects/', include('gungnir.projects.urls')),

    url(r'^admin/', include(admin.site.urls)),

    # celery task views
    url(r'^builds/tasks/build_image/(?P<build_config_id>\d+)$', build_image_view),



    # generic views
    (r'^AwsBaseAmi/$',AwsBaseAmiView.as_view()),
    (r'^BuildConfig/$',BuildConfigView.as_view()),
    (r'^Build/$',BuildView.as_view()),
    (r'^SupervisordCommand/$',SupervisordCommandView.as_view()),
    (r'^PythonRequirements/$',PythonRequirementsView.as_view()),

    # django-celery
    url(r'^celery/', include('djcelery.urls')),
    
    # django-registration - this is retarded how they suggest you override these. fact, you should just not include these urls...
    url(r'^accounts/register/$',
        'registration.views.register',
        {
            'backend': 'registration.backends.default.DefaultBackend',
            'form_class': CompatEmailUserCreationForm,
            'extra_context':{'page_title':'Create Account', 'page_header':'Create Account', 'form_submit_text':'Create'}
        },
        name='registration_register'),
    url(r'^accounts/login/$',
        'django.contrib.auth.views.login',
        {'authentication_form': CoreEmailAuthForm,},
        name='auth_login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='auth_logout'),
    # this has to be last, so stupid.
    (r'^accounts/', include('registration.backends.default.urls')),
)
