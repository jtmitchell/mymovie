# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from rest_framework_nested.routers import SimpleRouter, NestedSimpleRouter

from .views import MovieViewSet, WatchlistViewSet, NotificationViewSet

router = SimpleRouter(trailing_slash=False)
router.include_format_suffixes = False
router.register(r'v1/movies', MovieViewSet, base_name='movie')
router.register(r'v1/watchlists', WatchlistViewSet, base_name='watchlist')

# register the nested urls for movie routes
wl_router = NestedSimpleRouter(router, r'v1/watchlists',
                               lookup='watchlist', trailing_slash=False)
wl_router.register(r'notifications', NotificationViewSet,
                   base_name='notification')

urlpatterns = [
    url(r'', include(router.urls, namespace='movie')),
    url(r'', include(wl_router.urls, namespace='movie'))
]
