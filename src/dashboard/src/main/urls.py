from django.conf.urls.defaults import *
from django.conf import settings
from django.views.generic.simple import direct_to_template, redirect_to

UUID_REGEX = '[\w]{8}(-[\w]{4}){3}-[\w]{12}'

urlpatterns = patterns('dashboard.main.views',
  (r'sips/$', direct_to_template, {'template': 'main/sips.html', 'extra_context': {'polling_interval': settings.POLLING_INTERVAL, 'microservices_help': settings.MICROSERVICES_HELP}}, "sips"),
  (r'sips/go/$', 'sips'),
  (r'sips/go/(?P<uuid>' + UUID_REGEX + ')$', 'sips'),
  (r'jobs/(?P<uuid>' + UUID_REGEX + ')/explore/$', 'explore'),
  (r'tasks/(?P<uuid>' + UUID_REGEX + ')/$', 'tasks'),
  (r'', redirect_to, {'url': '/sips/'}),
)
