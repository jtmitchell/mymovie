"""
Empty registry model so we can use the Admin pages.
"""

from django.db import models


class EmailRegistryModel(models.Model):
    """
    Empty registry model to allow Admin pages.
    """

    class Meta:
        managed = False
        app_label = "email_registry"
