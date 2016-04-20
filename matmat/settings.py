import os
import dj_database_url
from django.conf import global_settings

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = os.getenv('SECRET_KEY', 'uevk2coz&16)x-r(5c_f0njs+9!$j&_(8)f20fa1*pu(&lvr08')

ON_SERVER = os.getenv('ON_SERVER', "False") == "True"
ON_DEV = os.getenv('ON_DEV', "False") == "True"
DEBUG = os.getenv('DJANGO_DEBUG', "False") == "True"

if not ON_SERVER:
    DEBUG = True
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['matmat.cz', 'www.matmat.cz', '*.matmat.cz']


ADMINS = (
    ('Jiří Řihák', 'exthran@gmail.com'),
)
EMAIL_SUBJECT_PREFIX = "[MatMat] "

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'lazysignup',
    'proso_ab',
    'proso_configab',
    'proso_common',
    'proso_models',
    'proso_user',
    'proso_feedback',
    'social.apps.django_app.default',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'proso_common.middleware.ToolbarMiddleware',
    'proso.django.request.RequestMiddleware',
    'proso.django.cache.RequestCacheMiddleware',
    'proso.django.log.RequestLogMiddleware',
    'proso_common.middleware.AuthAlreadyAssociatedMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'lazysignup.backends.LazySignupBackend',
    'social.backends.facebook.FacebookOAuth2',
    'social.backends.google.GoogleOAuth2',
)

ROOT_URLCONF = 'matmat.urls'

WSGI_APPLICATION = 'matmat.wsgi.application'


# Database
DATABASES = {"default": dj_database_url.config(default='postgresql://matmat:matmat@localhost/matmat')}

# Internationalization
LANGUAGE_CODE = 'cs-cz'
TIME_ZONE = 'Europe/Prague'
USE_I18N = True
USE_L10N = True
USE_TZ = False


# Static files (CSS, JavaScript, Images)
if ON_SERVER and not ON_DEV:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': '127.0.0.1:11211',
        }
    }

# Static files (CSS, JavaScript, Images)
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.CachedStaticFilesStorage'
STATIC_ROOT = os.path.join(BASE_DIR, '../static')
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

MEDIA_ROOT = os.path.join(BASE_DIR, '../media') if ON_SERVER else os.path.join(BASE_DIR, "media")
MEDIA_URL = '/media/'

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + [
   "proso_common.context_processors.config_processor",
]

SESSION_SERIALIZER='django.contrib.sessions.serializers.PickleSerializer'

DATA_DIR = os.environ.get('DATA_DIR', os.path.join(BASE_DIR, 'data'))

# Social auth
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.getenv("GOOGLE_OAUTH2_CLIENT_ID", "292645579868-u9e41sdmt269d7orrkq6j1cjhhudrgmq.apps.googleusercontent.com")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.getenv("GOOGLE_OAUTH2_CLIENT_SECRET", "WDLtIQEnvwHIy2ge96Uf3os-")
SOCIAL_AUTH_FACEBOOK_KEY = os.getenv('FACEBOOK_APP_ID', '300944176721659')
SOCIAL_AUTH_FACEBOOK_SECRET = os.getenv('FACEBOOK_API_SECRET', '5a4b653aba18f4b589d6003ec569efb3')
SOCIAL_AUTH_FACEBOOK_EXTENDED_PERMISSIONS = ['email']


# Debug toolbar
if DEBUG:
    INSTALLED_APPS += ('debug_toolbar',)
    MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)

if ON_SERVER:
    DEBUG_TOOLBAR_PATCH_SETTINGS = False
    # Sentry logging
    INSTALLED_APPS += ('raven.contrib.django.raven_compat',)
    RAVEN_CONFIG = {
        'dsn': os.getenv('RAVEN_DSN')
    }
else:
    LOGGING = {
        'version': 1,
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
            },
        },
        'loggers': {
            'django.request': {
                'handlers': ['console'],
                'propagate': True,
                'level': 'DEBUG',
            }
        },
    }

# Emails

EMAIL_SELF = 'web@matmat.cz'
EMAIL_CONTACT = 'matmat-web@googlegroups.com'
EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
