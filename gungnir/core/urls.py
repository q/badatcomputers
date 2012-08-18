from django.conf.urls import patterns, url

urlpatterns = patterns('gungnir.core.views',
    url(r'^test/$', 'index', 'core-index'),
)
