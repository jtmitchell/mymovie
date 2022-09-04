# -*- coding: utf-8 -*-
from django.urls import include, path
from rest_framework_nested.routers import SimpleRouter, NestedSimpleRouter

from .views import MovieViewSet, WatchlistViewSet, NotificationViewSet

router = SimpleRouter(trailing_slash=False)
router.include_format_suffixes = False
router.register(r"v1/movies", MovieViewSet, basename="movie")
router.register(r"v1/watchlists", WatchlistViewSet, basename="watchlist")

# register the nested urls for movie routes
wl_router = NestedSimpleRouter(
    router, "v1/watchlists", lookup="watchlist", trailing_slash=False
)
wl_router.register("notifications", NotificationViewSet, basename="notification")

urlpatterns = [path("", include(router.urls)), path("", include(wl_router.urls))]
