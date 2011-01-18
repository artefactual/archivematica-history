from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template, redirect_to

UUID_REGEX = '[\w]{8}(-[\w]{4}){3}-[\w]{12}'

urlpatterns = patterns('dashboard.main.views',

  (r'jobs/(?P<jobuuid>' + UUID_REGEX + ')/$', 'show_dir'),
  (r'jobs/(?P<jobuuid>' + UUID_REGEX + ')/(?P<subdir>.*)/$', 'show_subdir'),

  (r'sips/$', direct_to_template, {'template': 'main/sips.html'}, "sips"),
  (r'sips/all/$', 'get_all'),

  (r'', redirect_to, {'url': '/sips/'}),

)
