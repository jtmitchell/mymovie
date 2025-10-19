# flake8: noqa
# pylint: disable=wildcard-import, unused-wildcard-import

from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

from .base import *

DEBUG = True
TEMPLATE_DEBUG = True

INSTALLED_APPS += ["debug_toolbar"]

INTERNAL_IPS = ["127.0.0.1"]

MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]

ALLOWED_HOSTS = ["*"]

SECRET_KEY = get_env_variable("DJANGO_SECRET_KEY", "NOT_SECURE")

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    }
}
