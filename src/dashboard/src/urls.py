from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^mcp/', include('mcp.urls')),
    (r'^installer/', include('installer.urls')),
    (r'^administration/accounts/', include('accounts.urls')),
    (r'', include('main.urls')),
)
