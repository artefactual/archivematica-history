from django.conf.urls.defaults import *

urlpatterns = patterns('dashboard.mcp.views',
  (r'jobs-awaiting-approval/$', 'jobs_awaiting_approval'),
  (r'approve-job/$', 'approve_job'),
)
