from django.conf.urls.defaults import *
import dashboard.views

UUID_REGEX = '[\w]{8}(-[\w]{4}){3}-[\w]{12}'

urlpatterns = patterns('',

  (r'^$', dashboard.views.index),

  (r'^jobs/$', dashboard.views.jobs),
  (r'^jobs/page/(?P<page>\d+)/$', dashboard.views.jobs),

  (r'^jobs/(?P<jobuuid>' + UUID_REGEX + ')/$', dashboard.views.show_dir),
  (r'^jobs/(?P<jobuuid>' + UUID_REGEX + ')/(?P<subdir>.*)/$', dashboard.views.show_subdir),

  (r'^sips/$', dashboard.views.sips),

  (r'^tasks/$', dashboard.views.tasks),
  (r'^tasks/page/(?P<page>\d+)/$', dashboard.views.tasks),

  (r'client/$', dashboard.views.client),

  (r'mcp/jobs-awaiting-approval/$', dashboard.views.jobs_awaiting_approval),
  (r'mcp/approve-job/$', dashboard.views.approve_job),

)
