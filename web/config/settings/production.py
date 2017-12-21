# -*- coding: utf-8 -*-

from .common import *  # noqa

DEBUG = env.bool('DJANGO_DEBUG', default=False)

DEPLOYMENT = "production"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] \
%(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'WARNING',
        },
        'xproject': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'INFO',
        },
        'gensim.models': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'WARNING',
        },
        'root': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'WARNING',
        },
    }
}