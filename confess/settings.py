"""
Django settings for confess project.

Generated by 'django-admin startproject' using Django 1.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import environ

env = environ.Env(
    DEBUG=(bool, False)
)
environ.Env.read_env()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from celery.schedules import crontab

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY", default="ef+-3suc6+7wh%-n1hr71v83-5wvu7)dl8au#w9fe@4jd-af3#")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG", default=1)

ALLOWED_HOSTS = env("DJANGO_ALLOWED_HOSTS", default="*").split(" ")
# Application definition

INSTALLED_APPS = [
    'core',
    'confession',
    'vote',
    'voting',
    'comment',
    'reports',
    'admin_panel',
    'rule',
    'django_celery_beat',
    'rest_framework',
    # 'debug_toolbar',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'silk',
    'corsheaders'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
    # 'silk.middleware.SilkyMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'confess.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'confess.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    # 'default': {
    # 	'ENGINE': 'django.db.backends.sqlite3',
    # 	'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # },
    # "default": {
    #     "ENGINE": env("SQL_ENGINE", "django.db.backends.sqlite3"),
    #     "NAME": env("SQL_DATABASE", os.path.join(BASE_DIR, "db.sqlite3")),
    #     "USER": env("SQL_USER", "user"),
    #     "PASSWORD": env("SQL_PASSWORD", "password"),
    #     "HOST": env("SQL_HOST", "localhost"),
    #     "PORT": env("SQL_PORT", "5432"),
    # }
    "default": env.db("DATABASE_URL", default="sqlite://../db.sqlite3")
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

LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'UTC'
TIME_ZONE = 'Europe/Istanbul'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

# STATIC_ROOT = '/static/'

# REST_FRAMEWORK = {
# 	'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
# 	'PAGE_SIZE': 10
# }
#
# INTERNAL_IPS = [
# 	'127.0.0.1',
# ]

CORS_ORIGIN_ALLOW_ALL = True

# django_heroku.settings(locals())
# del DATABASES['default']['OPTIONS']['sslmode']

# PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
CELERY_BROKER_URL = env('CELERY_BROKER_URL', default='amqp://localhost:5672')
CELERY_TIMEZONE = 'Europe/Istanbul'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'default'
        },
    },
    'formatters': {
        'default': {
            'format': '[%(asctime)s %(levelname)s/%(processName)s/%(threadName)s] [%(name)s(%(funcName)s)(%(lineno)d)] %(message)s',
            'datefmt': "%Y-%m-%d %H:%M:%S"
        }
    },
    'loggers': {
        'confession': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False
        },
        'celery': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True
        },
    }
}

SLACK_TOKEN = env("SLACK_TOKEN", default="ZS1OTeWOOUeG2dXOIiCUQcpnyr27w0QT")  # default is mocked
SLACK_WEBHOOK = env("SLACK_WEBHOOK",
                    default="https://hooks.slack.com/services/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")
SLACK_CHANNEL = '#tasks'
SLACK_USERNAME = 'localhost'
