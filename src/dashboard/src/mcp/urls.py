from django.conf.urls.defaults import *

urlpatterns = patterns('dashboard.mcp.views',
  (r'approve-job/$', 'approve_job'),
  (r'jobs-awaiting-approval/$', 'jobs_awaiting_approval'),
  (r'reject-job/$', 'reject_job'),
)
