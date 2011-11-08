from django.conf.urls.defaults import *
from django.conf import settings
from django.views.generic.simple import direct_to_template, redirect_to

UUID_REGEX = '[\w]{8}(-[\w]{4}){3}-[\w]{12}'

urlpatterns = patterns('dashboard.main.views',

  # Index
  (r'^$', 'home'),

  # Transfer
  (r'transfer/$', 'transfer_grid'),
  (r'transfer/(?P<uuid>' + UUID_REGEX + ')/$', 'transfer_detail'),
  (r'transfer/status/$', 'transfer_status'),
  (r'transfer/status/(?P<uuid>' + UUID_REGEX + ')/$', 'transfer_status'),

  # Ingest
  (r'ingest/$', 'ingest_grid'),
  (r'ingest/(?P<uuid>' + UUID_REGEX + ')/$', 'ingest_detail'),
  (r'ingest/(?P<uuid>' + UUID_REGEX + ')/delete/$', 'ingest_delete'),
  (r'ingest/(?P<uuid>' + UUID_REGEX + ')/metadata/$', 'ingest_metadata'),
  (r'ingest/(?P<uuid>' + UUID_REGEX + ')/microservices/$', 'ingest_microservices'),
  (r'ingest/(?P<uuid>' + UUID_REGEX + ')/rights/$', 'ingest_rights'),
  (r'ingest/status/$', 'ingest_status'),
  (r'ingest/status/(?P<uuid>' + UUID_REGEX + ')/$', 'ingest_status'),
  # (r'ingest/metadata/(?P<uuid>' + UUID_REGEX + ')/$', 'ingest_metadata'),
  (r'ingest/normalization_report/(?P<uuid>' + UUID_REGEX + ')/$', 'ingest_normalization_report'),

  # Jobs and taks (is part of ingest)
  (r'jobs/(?P<uuid>' + UUID_REGEX + ')/explore/$', 'jobs_explore'),
  (r'jobs/(?P<uuid>' + UUID_REGEX + ')/list-objects/$', 'jobs_list_objects'),
  (r'jobs/(?P<uuid>' + UUID_REGEX + ')/manual-normalization/$', 'jobs_manual_normalization'),
  (r'tasks/(?P<uuid>' + UUID_REGEX + ')/$', 'tasks'),

  # Archival storage
  (r'archival-storage/$', 'archival_storage'),
  (r'archival-storage/(?P<path>AIPsStore/[0-9a-z]{4}/[0-9a-z]{3}/[0-9a-z]{4}/[0-9a-z]{4}/[0-9a-z]{4}/[0-9a-z]{4}/[0-9a-z]{4}/.*\.zip)/$', 'archival_storage'),

  # Preservation planning
  (r'preservation-planning/$', 'preservation_planning'),

  # Access
  (r'access/$', 'access'),

  # Settings
  (r'settings/$', 'settings'),

  #Status
  (r'status/$', 'status'),

)
