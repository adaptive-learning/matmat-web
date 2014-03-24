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
    'core',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
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
