from django.conf.urls.defaults import *

UUID_REGEX = '[\w]{8}(-[\w]{4}){3}-[\w]{12}'

urlpatterns = patterns('dashboard.main.views',
  (r'jobs/(?P<jobuuid>' + UUID_REGEX + ')/$', 'show_dir'),
  (r'jobs/(?P<jobuuid>' + UUID_REGEX + ')/(?P<subdir>.*)/$', 'show_subdir'),
  (r'sips/$', 'sips'),
  (r'sips/(?P<sipuuid>' + UUID_REGEX + ')/remove/$', 'remove_sip'),
  (r'tasks/(?P<jobuuid>' + UUID_REGEX + ')/$', 'tasks'),
  (r'', 'index'),
)
