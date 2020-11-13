import os
import sys

import dj_database_url
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(PROJECT_DIR)
BASE_DIR_NAME = os.path.basename(BASE_DIR)
DATA_DIR = os.path.join(BASE_DIR, '__data__')
SERVICE_NAME = os.environ.get('SERVICE_NAME', BASE_DIR_NAME)

DOMAIN = os.getenv('DOMAIN', 'https://suidp-stage.pik-software.ru')

SERVICE_TITLE = 'СУИДП'

AUTH_USER_MODEL = 'user_profile.User'

REDIS_URL = os.environ.get(
    'REDIS_URL',
    'redis://@127.0.0.1:6379')
DATABASE_URL = os.environ.get(
    'DATABASE_URL',
    'postgres://@127.0.0.1:5432/' + SERVICE_NAME)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
SECRET_KEY = os.environ.get('SECRET_KEY', '~+%iawwf2@R!@nakwe%jcAWKJF1asdAFw2')

ENVIRONMENT = os.environ.get('ENVIRONMENT', 'staging')

ALLOWED_HOSTS = ['*']
INTERNAL_IPS = ['127.0.0.1']

# ------------------ #
# --- <SERVICES> --- #

# SENTRY
if not DEBUG and ENVIRONMENT not in ['development', 'test']:
    sentry_sdk.init(
        dsn="https://21ac2b66046d4ff282f9ef2f7a80eff5@sentry.apiqa.dev/32",
        integrations=[DjangoIntegration()],
        environment=ENVIRONMENT
    )


# --- </SERVICES> --- #
# ------------------- #

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',

    '_project_',

    # APPS
    'user_profile',

    # HISTORY
    'simple_history',

    # Django health check
    'health_check',  # required
    'health_check.db',  # stock Django health checkers
    'health_check.cache',
    'health_check.storage',
    'health_check.contrib.celery',  # requires celery

    # DEV
    'debug_toolbar',
    'django_extensions',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # HISTORY
    'simple_history.middleware.HistoryRequestMiddleware',

    # DEV
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

WSGI_APPLICATION = '_project_.wsgi.application'
ROOT_URLCONF = '_project_.urls'

TEMPLATE_ACCESSIBLE_SETTINGS = ['DEBUG', 'MEDIA_URL', 'SERVICE_TITLE']
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(PROJECT_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.media',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.settings',
            ],
        },
    },
]

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.parse(
        DATABASE_URL,
        engine='django.db.backends.postgresql'
    )
}
DATABASES['default']['ATOMIC_REQUESTS'] = True


CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        },
        "KEY_PREFIX": SERVICE_NAME
    },
    "sessions": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"{REDIS_URL}/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
        "KEY_PREFIX": SERVICE_NAME
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.'
             'UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.'
             'MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.'
             'CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.'
             'NumericPasswordValidator'},
]

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'ru-RU'  # 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False

DATE_INPUT_FORMATS = [
    '%Y-%m-%d', '%m/%d/%Y',   # '2006-10-25', '10/25/2006',
    '%m/%d/%y',               # '10/25/06'
    '%b %d %Y', '%b %d, %Y',  # 'Oct 25 2006', 'Oct 25, 2006'
    '%d %b %Y', '%d %b, %Y',  # '25 Oct 2006', '25 Oct, 2006'
    '%B %d %Y', '%B %d, %Y',  # 'October 25 2006', 'October 25, 2006'
    '%d %B %Y', '%d %B, %Y',  # '25 October 2006', '25 October, 2006'
    '%d.%m.%Y',               # '25.10.2006'
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.environ.get('STATIC_ROOT', os.path.join(DATA_DIR, 'static'))
STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, 'static'),
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.environ.get('MEDIA_ROOT', os.path.join(DATA_DIR, 'media'))

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'sessions'

LOGIN_REDIRECT_URL = '/'
INDEX_STAFF_REDIRECT_URL = '/admin/'
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

# storage
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'


ONLY_LAST_VERSION_ALLOWED_DAYS_RANGE = os.environ.get(
    'ONLY_LAST_VERSION_ALLOWED_DAYS_RANGE', 1)
SOFT_DELETE_SAFE_MODE = False

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'root': {
        'level': 'WARNING',
        'handlers': ['console'],
    },
    'formatters': {
        'verbose': {
            'format': '[django] %(levelname)s %(asctime)s %(name)s/%(module)s %(process)d/%(thread)d: %(message)s'  # noqa
        }
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'level': 'INFO',
            'handlers': ['console'],
            'propagate': True,
        },
    },
}


try:
    from .settings_local import *  # noqa: pylint=unused-wildcard-import, pylint=wildcard-import
except ImportError:
    pass
