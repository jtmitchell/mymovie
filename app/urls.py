"""mymovie URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import RedirectView

from .views import ConfigurationView
from app.views import HomepageView


urlpatterns = [
    url(r'^favicon\.ico$',
        RedirectView.as_view(
            url='/static/app/favicon.png',
            permanent=False,
            ),
        name='favicon'),
    url(r'^robots\.txt$',
        RedirectView.as_view(
            url='/static/app/robots.txt',
            permanent=False,
            ),
        name='robots'),

    url(r'^[/]?$',
        HomepageView.as_view(),
        kwargs=dict(title='MyMovie | Coming soon...'),
        name='homepage'),

    url(r'^api/v1/config',
        ConfigurationView.as_view(), name='configuration'),

    url(r'^api/', include('users.urls', namespace='api')),
    url(r'^api/', include('movies.urls', namespace='api')),

    url(r'^api-auth',
        include('rest_framework.urls', namespace='rest_framework')),

    url('', include('social_django.urls', namespace='social')),

    url(r'^admin/', include(admin.site.urls)),
]
