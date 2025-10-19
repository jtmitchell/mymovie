# flake8: noqa
# pylint: disable=wildcard-import, unused-wildcard-import
import os

if "DJANGO_SECRET_KEY" not in os.environ:
    from django.core.management.utils import get_random_secret_key

    os.environ["DJANGO_SECRET_KEY"] = get_random_secret_key()

from .base import *

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": f"{BASE_DIR}/db.sqlite3",
    }
}

# Use a fast hasher to speed up tests.
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    }
}

LOGGING = {}
