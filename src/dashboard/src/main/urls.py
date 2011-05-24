from django.conf.urls.defaults import *
from django.conf import settings
from django.views.generic.simple import direct_to_template, redirect_to

UUID_REGEX = '[\w]{8}(-[\w]{4}){3}-[\w]{12}'

urlpatterns = patterns('dashboard.main.views',

  # Index
  (r'^$', redirect_to, {'url': '/ingest/'}),

  # Ingest
  url(r'ingest/$', direct_to_template, {'template': 'main/ingest.html', 'extra_context': {'polling_interval': settings.POLLING_INTERVAL, 'microservices_help': settings.MICROSERVICES_HELP}}, 'ingest'),
  (r'ingest/go/$', 'ingest'),
  (r'ingest/go/(?P<uuid>' + UUID_REGEX + ')$', 'ingest'),
  (r'jobs/(?P<uuid>' + UUID_REGEX + ')/explore/$', 'explore'),
  (r'jobs/(?P<uuid>' + UUID_REGEX + ')/list-objects/$', 'list_objects'),
  (r'jobs/(?P<uuid>' + UUID_REGEX + ')/manual-normalization/$', 'manual_normalization'),
  (r'tasks/(?P<uuid>' + UUID_REGEX + ')/$', 'tasks'),

  # Preservatin planning
  (r'preservation-planning/$', 'preservation_planning'),

)
