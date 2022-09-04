"""
mymovie URL Configuration.
"""
from django.urls import include, path
from django.contrib import admin
from django.views.generic.base import RedirectView
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view
from rest_framework import permissions
from rest_framework.schemas.openapi import SchemaGenerator

from app.views import HomepageView
from .views import ConfigurationView


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
    path("api/v1/", include("users.urls")),
    path("api/v1/", include("movies.urls")),
    path(
        "api-auth",
        include(
            "rest_framework.urls",
        ),
    ),
    path("", include("social_django.urls")),
    path("admin/", admin.site.urls),
    # Add an OpenAPI/Swagger schema endpoint
    # This will generate and return the YAML for our API
    path(
        "/api/openapi",
        get_schema_view(
            title="MyMovies API",
            description="API endpoints for MyMovies",
            version="1.0.0",
            url="/api/v1",
            public=True,
            permission_classes=[permissions.AllowAny],
            # urlconf="",
            generator_class=SchemaGenerator,
        ),
        name="openapi-schema-v1",
    ),
    path(
        "/api/openapi/docs",
        TemplateView.as_view(
            template_name="openapi/swagger-ui.html",
            extra_context={
                "schema_url": "openapi-schema-v1",
                "title": "MyMovie OpenAPI",
            },
        ),
        name="swagger-ui",
    ),
]
