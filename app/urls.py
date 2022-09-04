"""
mymovie URL Configuration.
"""
from django.urls import include, path
from django.contrib import admin
from django.views.generic.base import RedirectView

from .views import ConfigurationView
from app.views import HomepageView


urlpatterns = [
    path(
        "favicon.ico",
        RedirectView.as_view(
            url="/static/app/favicon.png",
            permanent=False,
        ),
        name="favicon",
    ),
    path(
        "robots.txt",
        RedirectView.as_view(
            url="/static/app/robots.txt",
            permanent=False,
        ),
        name="robots",
    ),
    path(
        "/",
        HomepageView.as_view(),
        kwargs=dict(title="MyMovie | Coming soon..."),
        name="homepage",
    ),
    path("api/v1/config", ConfigurationView.as_view(), name="configuration"),
    path("api/", include("users.urls")),
    path("api/", include("movies.urls")),
    path(
        "api-auth",
        include(
            "rest_framework.urls",
        ),
    ),
    path("", include("social_django.urls")),
    path("admin/", admin.site.urls),
]
