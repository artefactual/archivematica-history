from django.conf.urls.defaults import patterns

urlpatterns = patterns('installer.views',
    (r'welcome/$', 'welcome'),
)
