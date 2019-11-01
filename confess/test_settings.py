import os

from confess.settings import *

SECRET_KEY = "ef+-3suc6+7wh%-n1hr71v83-5wvu7)dl8au#w9fe@4jd-af3#"
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

DEBUG = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'default': {
            'format': '[%(asctime)s %(levelname)s/%(processName)s/%(threadName)s] [%(name)s(%(funcName)s)(%(lineno)d)] %(message)s',
            'datefmt': "%Y-%b-%d %H:%M:%S"
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'DEBUG'
        },
    }
}
