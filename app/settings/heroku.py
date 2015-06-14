# -*- coding: utf-8 -*-

import dj_database_url

from .base import *

DEBUG = False
TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ['.herokuapp.com',
                 '.maungawhau.net.nz'
                 ]

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Parse database configuration from $DATABASE_URL
DATABASES['default'] = dj_database_url.config()
