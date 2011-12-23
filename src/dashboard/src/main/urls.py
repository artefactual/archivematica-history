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
    (r'transfer/(?P<uuid>' + UUID_REGEX + ')/delete/$', 'transfer_delete'),
    (r'transfer/(?P<uuid>' + UUID_REGEX + ')/microservices/$', 'transfer_microservices'),
    (r'transfer/(?P<uuid>' + UUID_REGEX + ')/rights/$', 'transfer_rights_list'),
    (r'transfer/(?P<uuid>' + UUID_REGEX + ')/rights/add/$', 'transfer_rights_edit'),
    (r'transfer/(?P<uuid>' + UUID_REGEX + ')/rights/(?P<id>\d+)/$', 'transfer_rights_edit'),
    (r'transfer/(?P<uuid>' + UUID_REGEX + ')/rights/delete/(?P<id>\d+)/$', 'transfer_rights_delete'),
    (r'transfer/status/$', 'transfer_status'),
    (r'transfer/status/(?P<uuid>' + UUID_REGEX + ')/$', 'transfer_status'),

    # Ingest
    (r'ingest/$', 'ingest_grid'),
    (r'ingest/(?P<uuid>' + UUID_REGEX + ')/$', 'ingest_detail'),
    (r'ingest/(?P<uuid>' + UUID_REGEX + ')/delete/$', 'ingest_delete'),
    (r'ingest/(?P<uuid>' + UUID_REGEX + ')/metadata/$', 'ingest_metadata'),
    (r'ingest/(?P<uuid>' + UUID_REGEX + ')/microservices/$', 'ingest_microservices'),
    (r'ingest/(?P<uuid>' + UUID_REGEX + ')/rights/$', 'ingest_rights_list'),
    (r'ingest/(?P<uuid>' + UUID_REGEX + ')/rights/add/$', 'ingest_rights_edit'),
    (r'ingest/(?P<uuid>' + UUID_REGEX + ')/rights/(?P<id>\d+)/$', 'ingest_rights_edit'),
    (r'ingest/status/$', 'ingest_status'),
    (r'ingest/status/(?P<uuid>' + UUID_REGEX + ')/$', 'ingest_status'),
    (r'ingest/normalization-report/(?P<uuid>' + UUID_REGEX + ')/$', 'ingest_normalization_report'),

    # Jobs and taks (is part of ingest)
    (r'jobs/(?P<uuid>' + UUID_REGEX + ')/explore/$', 'jobs_explore'),
    (r'jobs/(?P<uuid>' + UUID_REGEX + ')/list-objects/$', 'jobs_list_objects'),
    (r'tasks/(?P<uuid>' + UUID_REGEX + ')/$', 'tasks'),

    # Archival storage
    (r'archival-storage/$', 'archival_storage'),
    (r'archival-storage/(?P<path>AIPsStore/[0-9a-z]{4}/[0-9a-z]{3}/[0-9a-z]{4}/[0-9a-z]{4}/[0-9a-z]{4}/[0-9a-z]{4}/[0-9a-z]{4}/.*\.(7z|zip))/$', 'archival_storage'),

    # Preservation planning
    (r'preservation-planning/$', 'preservation_planning'),

    # Access
    (r'access/$', 'access_list'),
    (r'access/(?P<id>\d+)/delete/$', 'access_delete'),

    # Lookup
    (r'lookup/rightsholder/(?P<id>\d+)/$', 'rights_holders_lookup'),

    # Autocomplete
    (r'autocomplete/rightsholders$', 'rights_holders_autocomplete'),

    # Settings
    (r'settings/$', 'settings_list'),
    (r'settings/(?P<id>\d+)/$', 'settings_edit'),

    #Status
    (r'status/$', 'status'),

)
