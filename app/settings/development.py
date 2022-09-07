# flake8: noqa
# pylint: disable=wildcard-import, unused-wildcard-import

from .base import *

DEBUG = True
TEMPLATE_DEBUG = True

INSTALLED_APPS += ["debug_toolbar"]

INTERNAL_IPS = ["127.0.0.1"]

MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]

ALLOWED_HOSTS = ["*"]

SECRET_KEY = get_env_variable("DJANGO_SECRET_KEY", "NOT_SECURE")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": f"{BASE_DIR}/db.sqlite3",
    }
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    }
}
