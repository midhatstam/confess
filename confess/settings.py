"""
Django settings for confess project.

Generated by 'django-admin startproject' using Django 1.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
# import django_heroku

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "ef+-3suc6+7wh%-n1hr71v83-5wvu7)dl8au#w9fe@4jd-af3#"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = int(os.environ.get("DEBUG", default=1))

#ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", default="konfessproject.herokuapp.com").split(" ")
ALLOWED_HOSTS = ["*"]
# Application definition

INSTALLED_APPS = [
	'core',
	'confession',
	'vote',
	'voting',
	'comment',
	'reports',
	'admin_panel',
	'rest_framework',
	# 'debug_toolbar',
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'silk',
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
	'silk.middleware.SilkyMiddleware',
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
	"default": {
		"ENGINE": os.environ.get("SQL_ENGINE", "django.db.backends.sqlite3"),
		"NAME": os.environ.get("SQL_DATABASE", os.path.join(BASE_DIR, "db.sqlite3")),
		"USER": os.environ.get("SQL_USER", "user"),
		"PASSWORD": os.environ.get("SQL_PASSWORD", "password"),
		"HOST": os.environ.get("SQL_HOST", "localhost"),
		"PORT": os.environ.get("SQL_PORT", "5432"),
	}
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

STATICFILES_DIRS = [
	os.path.join(BASE_DIR, "static")
]

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

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
