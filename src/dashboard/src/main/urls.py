from django.conf.urls.defaults import *
from django.conf import settings
from django.views.generic.simple import direct_to_template, redirect_to

UUID_REGEX = '[\w]{8}(-[\w]{4}){3}-[\w]{12}'

urlpatterns = patterns('dashboard.main.views',

  # Index
  (r'^$', redirect_to, {'url': '/ingest/'}),

  # Transfer
  (r'transfer/$', 'transfer_base'),
  (r'transfer/go/$', 'transfer'),
  (r'transfer/go/(?P<uuid>' + UUID_REGEX + ')/$', 'transfer'),

  # Ingest
  (r'ingest/$', 'ingest_base'),
  (r'ingest/metadata/(?P<uuid>' + UUID_REGEX + ')/$', 'ingest_metadata'),
  (r'ingest/go/$', 'ingest'),
  (r'ingest/go/(?P<uuid>' + UUID_REGEX + ')$', 'ingest'),
  (r'ingest/(?P<uuid>' + UUID_REGEX + ')/normalization-report$', 'normalization_report'),
  (r'jobs/(?P<uuid>' + UUID_REGEX + ')/explore/$', 'explore'),
  (r'jobs/(?P<uuid>' + UUID_REGEX + ')/list-objects$', 'list_objects'),
  (r'jobs/(?P<uuid>' + UUID_REGEX + ')/manual-normalization$', 'manual_normalization'),
  (r'tasks/(?P<uuid>' + UUID_REGEX + ')/$', 'tasks'),

  # Archival storage
  (r'archival-storage/$', 'archival_storage'),
  (r'archival-storage/(?P<path>AIPsStore/[0-9a-z]{4}/[0-9a-z]{3}/[0-9a-z]{4}/[0-9a-z]{4}/[0-9a-z]{4}/[0-9a-z]{4}/[0-9a-z]{4}/.*\.zip)$', 'archival_storage'),

  # Preservation planning
  (r'preservation-planning/$', 'preservation_planning'),

  # Access
  (r'access/$', 'access'),

  # Settings
  (r'settings/$', 'settings'),

)
