"""
Registry for email functions.
"""

from django.contrib import admin
from django.urls import path

from .models import EmailRegistryModel
from .views import EmailsView, EmailTestView


@admin.register(EmailRegistryModel)
class EmailRegistryAdmin(admin.ModelAdmin):
    """
    Registry for email functions.
    """
    def get_urls(self):
        """
        Add admin urls.
        """
        opts = self.model._meta
        return [
            path(
                "",
                self.admin_site.admin_view(EmailsView.as_view(extra_context={"opts": opts})),
                name="email_registry_emailregistrymodel_changelist",
            ),
            path("preview/<str:identifier>/", EmailTestView.as_view(), name="preview_email"),
        ]
