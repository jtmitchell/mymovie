# flake8: noqa
# pylint: disable=wildcard-import, unused-wildcard-import

from .base import *

DEBUG = False
TEMPLATE_DEBUG = False

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
