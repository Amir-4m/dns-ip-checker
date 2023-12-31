"""
Django settings for dns_ip_domain project.

Generated by 'django-admin startproject' using Django 1.11.17.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import logging.config
from .local_settings import *

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '2-8n!d^qmck+c+o$+4&=_=o8p1gimu6c3j-ircfap008w*scsz'

# Application definition
INSTALLED_APPS = [
    'dns_updater',
    'domain_check',
    'ping_logs',
    'tel_tools',
    'notifier',
    'promoter',

    'import_export',
    'django_celery_beat',
    'rest_framework',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'dns_ip_domain.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        # 'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'loaders': [
                ('django.template.loaders.cached.Loader', [
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                ]),
            ],
        },
    },
]

WSGI_APPLICATION = 'dns_ip_domain.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

#
DATABASES = {
    'default': {
        'ENGINE': DB_ENGINE,
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASS,
        'HOST': DB_HOST,
        'PORT': DB_PORT,
        # 'OPTIONS': {'charset': 'utf8mb4'}
    },
    'telegram-mtproxy-bot': {
        'ENGINE': DB_ENGINE,
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASS,
        'HOST': DB_HOST,
        'PORT': DB_PORT,
        'OPTIONS': {'charset': 'utf8mb4'}
    }
}

CACHES = {
    'default': {
        'BACKEND': CACHE_BACKEND,
        'LOCATION': CACHE_HOST,
        'KEY_PREFIX': 'DNS_IP_DOMAIN'  # Todo change key_prefix
    },
}

CELERY_BROKER_URL = 'amqp://%(USER)s:%(PASS)s@%(HOST)s' % {
    'USER': CELERY_BROKER_USER,
    'PASS': CELERY_BROKER_PASS,
    'HOST': CELERY_BROKER_HOST,
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/
USE_TZ = True
TIME_ZONE = 'Asia/Tehran'

LANGUAGE_CODE = 'en-us'
USE_I18N = True
USE_L10N = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

LOG_DIR = os.path.join(BASE_DIR, 'logs')
LOGGING = ({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '[%(asctime)s] %(levelname)s %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'verbose': {
            'format': '[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'WARNING',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'DEBUG' if DEBUG else 'INFO',
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': os.path.join(LOG_DIR, 'django.log'),
        },
    },
    'loggers': {
        'domain_check': {
            'level': 'DEBUG',
            'handlers': ['console', 'file']
        },
        'dns_updater': {
            'level': 'DEBUG',
            'handlers': ['file']
        },
        'promoter': {
            'level': 'WARNING',
            'handlers': ['console'],
            'propagate': False,
        },
        'promoter.tasks': {
            'level': 'DEBUG',
            'handlers': ['console', 'file']
        },
        'notifier': {
            'level': 'DEBUG',
            'handlers': ['console', 'file']
        },
        'tel_tools': {
            'level': 'DEBUG',
            'handlers': ['console', 'file']
        },
    }
})

# IMPORT_EXPORT_USE_TRANSACTIONS = True
# IMPORT_EXPORT_SKIP_ADMIN_LOG = True
