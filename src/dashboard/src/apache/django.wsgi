import os, sys
import django.core.handlers.wsgi

# Ensure that the path does not get added multiple times
path = '/usr/local/share'
if path not in sys.path:
  sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'dashboard.settings'

application = django.core.handlers.wsgi.WSGIHandler()

# See http://blog.dscpl.com.au/2008/12/using-modwsgi-when-developing-django.html
from django.conf import settings
if settings.DEBUG:
  import dashboard.monitor
  dashboard.monitor.start(interval=1.0)
