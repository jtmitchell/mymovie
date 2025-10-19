"""
Custom admin site.
"""

from django.conf import settings
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse


class AdminSite(admin.AdminSite):
    """
    Custom admin site.
    """

    site_header = "Administration"
    site_title = site_header
    index_title = site_header

    def login(self, request, *args, **kwargs):
        """Use the django-allauth login."""
        urlparams = [f"{k}={v}" for k, v in request.GET.items()]
        login_url = reverse(settings.LOGIN_URL)
        if urlparams:
            return redirect(f"{login_url}?{'&'.join(urlparams)}")
        return redirect(login_url)
