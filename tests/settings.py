from confess.settings import *

SECRET_KEY = "ef+-3suc6+7wh%-n1hr71v83-5wvu7)dl8au#w9fe@4jd-af3#"
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'test-db.sqlite3'),
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

NOSE_ARGS = ["--with-coverage", "--cover-package=admin_panel,comment,confession,reports,rule,voting", "--with-xunit", "--cover-erase"]
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
