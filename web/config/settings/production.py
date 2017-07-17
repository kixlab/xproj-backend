# -*- coding: utf-8 -*-

from .common import *  # noqa

DEBUG = env.bool('DJANGO_DEBUG', default=False)

DEPLOYMENT = "production"

ALLOWED_HOSTS = ['*']