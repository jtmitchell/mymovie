# -*- coding: utf-8 -*-

from .base import *

DEBUG = True
TEMPLATE_DEBUG = True

INSTALLED_APPS += ("debug_toolbar",)

INTERNAL_IPS = ("127.0.0.1",)

MIDDLEWARE += ("debug_toolbar.middleware.DebugToolbarMiddleware",)

ALLOWED_HOSTS = ["*"]

SECRET_KEY = get_env_variable("DJANGO_SECRET_KEY", "NOT_SECURE")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": path_root("db.sqlite3"),
    }
}
