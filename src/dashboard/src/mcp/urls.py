from django.conf.urls.defaults import *

urlpatterns = patterns('dashboard.mcp.views',
  (r'execute/$', 'execute'),
  (r'list/$', 'list'),
)
