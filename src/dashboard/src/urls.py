from django.conf.urls.defaults import *
import dashboard.views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',

  # Example:
  # (r'^app/', include('app.foo.urls')),

  # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
  # to INSTALLED_APPS to enable admin documentation:
  # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

  # Uncomment the next line to enable the admin:
  # (r'^admin/', include(admin.site.urls)),

  (r'^$', dashboard.views.index),

  (r'^jobs/$', dashboard.views.jobs),
  (r'^jobs/page/(?P<page>\d+)/$', dashboard.views.jobs),

  (r'^sips/$', dashboard.views.sips),

  (r'^tasks/$', dashboard.views.tasks),
  (r'^tasks/page/(?P<page>\d+)/$', dashboard.views.tasks),

  (r'client/$', dashboard.views.client),

  (r'mcp/jobs-awaiting-approval/$', dashboard.views.jobs_awaiting_approval),
  (r'mcp/approve-job/$', dashboard.views.approve_job),

)
