import os

BASE_PATH = os.path.dirname(__file__)

# Django settings for app project.

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'MCP',                        # Or path to database file if using sqlite3.
        'USER': 'demo',                       # Not used with sqlite3.
        'PASSWORD': 'demo',                   # Not used with sqlite3.
        'HOST': '',                           # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                           # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(BASE_PATH, 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/media/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/media/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    ('js', os.path.join(BASE_PATH, 'media', 'js')),
    ('css', os.path.join(BASE_PATH, 'media', 'css')),
    ('images', os.path.join(BASE_PATH, 'media', 'images')),
    ('vendor', os.path.join(BASE_PATH, 'media', 'vendor')),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'e7b-$#-3fgu)j1k01)3tp@^e0=yv1hlcc4k-b6*ap^zezv2$48'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    # 'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
#    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'middleware.common.AJAXSimpleExceptionResponseMiddleware',
    'installer.middleware.ConfigurationCheckMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_PATH, 'templates'),
)

INSTALLED_APPS = (
    # Django basics
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    # django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.webdesign',

    # Uncomment the next line to enable the admin:
    # 'django.contrib.admin',

    # Internal apps
    'installer',
    'accounts',
    'main',
    'mcp',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
      'mail_admins': {
        'level': 'ERROR',
        'class': 'django.utils.log.AdminEmailHandler'
      }
    },
    'loggers': {
      'django.request': {
        'handlers': ['mail_admins'],
        'level': 'ERROR',
        'propagate': True,
      },
    }
}

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/administration/accounts/login'

# Django debug toolbar
try:
    import debug_toolbar
except:
    pass
else:
    MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
    INSTALLED_APPS += ('debug_toolbar',)
    INTERNAL_IPS = ('127.0.0.1', '192.168.82.1', '10.0.2.2')
    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
    }

# Dashboard internal settings
MCP_SERVER = ('127.0.0.1', 4730) # localhost:4730
POLLING_INTERVAL = 5 # Seconds
STATUS_POLLING_INTERVAL = 5 # Seconds

MICROSERVICES_HELP = {
    'Approve transfer': 'Once you have added files to the transfer in the file browser, select "Transfer complete" to begin processing.',
    'Workflow decision - create transfer backup': 'Create a complete backup of the transfer in case transfer/ingest are interrupted or fail. The transfer will automatically be deleted once the AIP has been moved into storage.',
    'Workflow decision - send transfer to quarantine': 'If desired, quarantine transfer to allow definitions in anti-virus software to be updated.',
    'Remove from quarantine': 'If desired, select "Unquarantine" to remove the transfer from quarantine immediately. Otherwise, wait until the quarantine period has expired and the transfer will be removed automatically.',
    'Create SIP(s)': 'Create one or more SIPs from the transfer. See the Archivematica user manual for information about SIP creation options.',
    'Approve SIP Creation': 'Once you have added files from the transfer to the SIP and have completed any appraisal and physical arrangement, select "SIP creation complete" to start ingest micro-services.',
    'Normalize': 'Create preservation and/or access copies of files if desired. Creating access copies will result in a DIP being generated for upload into an access system.',
    'Approve normalization': 'In the file browser, review normalized files if desired.',
    'Store AIP': 'If desired, review AIP contents. Click "Store AIP" to move the AIP into archival storage.',
    'UploadDIP': 'If desired, review the DIP and remove any access copies that should not be uploaded to the public access system, e.g. for copyright or security reasons. Select "Upload DIP" to upload the DIP to the access system.',
}

try:
    LOCAL_SETTINGS
except NameError:
    try:
        from settings_local import *
    except ImportError:
        pass
