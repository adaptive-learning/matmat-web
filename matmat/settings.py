"""
Django settings for matmat project.
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import dj_database_url
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = 'uevk2coz&16)x-r(5c_f0njs+9!$j&_(8)f20fa1*pu(&lvr08'

ON_VIPER = os.getenv('ON_VIPER', "False") == "True"
DEBUG = os.getenv('DJANGO_DEBUG', "False") == "True"

if not ON_VIPER:
    DEBUG = True
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['matmat.cz', 'matmat.thran.cz']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'south',
    'lazysignup',
    'social_auth',
    'core',
    'model',
    'questions',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'core.middleware.AuthAlreadyAssociatedMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'lazysignup.backends.LazySignupBackend',
    'social_auth.backends.facebook.FacebookBackend',
    'social_auth.backends.google.GoogleOAuth2Backend',
)

ROOT_URLCONF = 'matmat.urls'

WSGI_APPLICATION = 'matmat.wsgi.application'


# Database

DATABASES = {"default": dj_database_url.config(default='mysql://matmat:poklop@localhost/matmat')}

# Internationalization

LANGUAGE_CODE = 'cs-cz'

TIME_ZONE = 'Europe/Prague'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_ROOT = os.path.join(BASE_DIR, '../static')
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

SESSION_SERIALIZER='django.contrib.sessions.serializers.PickleSerializer'

# Social auth
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/close_login_popup/'

# oauth2 data for localhost
GOOGLE_OAUTH2_CLIENT_ID = os.getenv("GOOGLE_OAUTH2_CLIENT_ID", "292645579868-u9e41sdmt269d7orrkq6j1cjhhudrgmq.apps.googleusercontent.com")
GOOGLE_OAUTH2_CLIENT_SECRET = os.getenv("GOOGLE_OAUTH2_CLIENT_SECRET", "WDLtIQEnvwHIy2ge96Uf3os-")
FACEBOOK_APP_ID = os.getenv('FACEBOOK_APP_ID', '300944176721659')
FACEBOOK_API_SECRET = os.getenv('FACEBOOK_API_SECRET', '5a4b653aba18f4b589d6003ec569efb3')
