from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse_lazy

from django.views.generic import TemplateView, RedirectView

urlpatterns = patterns('gungnir.core.views',
    url(r'^$', RedirectView.as_view(url=reverse_lazy('gungnir-core-about')), name='gungnir-core-index'),
    url(r'^about/$', TemplateView.as_view(template_name='core/about.html'), name='gungnir-core-about'),
)
#urlpatterns = patterns('gungnir.core.views',
#    url(r'^test/$', TemplateView.as_view(template_name='core/about.html') , 'core-index'),
#)
#
#urlpatterns = patterns('django.contrib.flatpages.views',
#    url(r'^about/$', 'flatpage', {'url': '/about/'}, name='about'),
