import os, sys
import django.core.handlers.wsgi

# Ensure that the path does not get added multiple times
path = '/var/www'
if path not in sys.path:
  sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'dashboard.settings'

application = django.core.handlers.wsgi.WSGIHandler()
