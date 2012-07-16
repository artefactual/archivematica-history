from django.conf.urls.defaults import patterns

urlpatterns = patterns('',
    (r'^$', 'accounts.views.list'),
    (r'add/$', 'accounts.views.add'),
    (r'(?P<id>\d+)/delete/$', 'accounts.views.delete'),
    (r'(?P<id>\d+)/edit/$', 'accounts.views.edit'),
    (r'profile/$', 'accounts.views.edit'),
    (r'list/$', 'accounts.views.list'),
    (r'login/$', 'django.contrib.auth.views.login', { 'template_name': 'accounts/login.html' }),
    (r'logout/$', 'django.contrib.auth.views.logout_then_login'),
)
