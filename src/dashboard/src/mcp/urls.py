from django.conf.urls.defaults import *

urlpatterns = patterns('mcp.views',
    (r'execute/$', 'execute'),
    (r'list/$', 'list'),
)
