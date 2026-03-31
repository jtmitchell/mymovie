# django-appconf configuration settings
import os

from appconf import AppConf as AppSettingsConf
from django.conf import settings  # noqa


class MoviesSettingsConf(AppSettingsConf):
    OMDB_API_KEY = os.environ.get("OMDB_API_KEY", "")

    class Meta:
        prefix = "movies"
