import os, sys
import django.core.handlers.wsgi

sys.path.append('/var/www')

os.environ['DJANGO_SETTINGS_MODULE'] = 'dashboard.settings'

application = django.core.handlers.wsgi.WSGIHandler()
