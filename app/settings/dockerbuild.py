# flake8: noqa
# pylint: disable=wildcard-import, unused-wildcard-import
"""
Minimal settings for Docker build to run collect static.

DO NOT USE THIS IN PRODUCTION!

"""
import os

if "DJANGO_SECRET_KEY" not in os.environ:
    from django.core.management.utils import get_random_secret_key

    os.environ["DJANGO_SECRET_KEY"] = get_random_secret_key()

from .base import *
