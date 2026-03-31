# django-appconf configuration settings
from appconf import AppConf as AppSettingsConf
from django.conf import settings


class EmailRegistrySettingsConf(AppSettingsConf):
    DEFAULT_FROM_EMAIL = settings.DEFAULT_FROM_EMAIL or "no-reply@example.company"
    FROM_EMAIL = DEFAULT_FROM_EMAIL
    ADMINS = settings.ADMINS or [("Admin", "admin@example.company")]
    MANAGERS = ADMINS

    class Meta:
        prefix = "emails"
