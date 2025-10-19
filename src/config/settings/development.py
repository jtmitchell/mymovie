# ruff: noqa: F403,F405
from .base import *

DEBUG = True
TEMPLATE_DEBUG = True

INSTALLED_APPS += ("debug_toolbar",)
INTERNAL_IPS = ("127.0.0.1",)

MIDDLEWARE += ("debug_toolbar.middleware.DebugToolbarMiddleware",)

ALLOWED_HOSTS = [".localhost", "127.0.0.1"]
CSRF_TRUSTED_ORIGINS = ["https://*.localhost"]