from django.conf.urls.defaults import *

urlpatterns = patterns('',
  (r'^mcp/', include('dashboard.mcp.urls')),
  (r'', include('dashboard.main.urls')),
)
