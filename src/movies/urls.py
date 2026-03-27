"""
Urls for the movie models.
"""

from django.urls import include, path
from rest_framework_nested.routers import NestedSimpleRouter, SimpleRouter  # type: ignore

from .views import MovieViewSet, NotificationViewSet, WatchlistViewSet

router = SimpleRouter(trailing_slash=False)
router.include_format_suffixes = False
router.register("movies", MovieViewSet, basename="movie")
router.register("watchlists", WatchlistViewSet, basename="watchlist")

# register the nested urls for movie routes
wl_router = NestedSimpleRouter(router, "watchlists", lookup="watchlist", trailing_slash=False)
wl_router.register("notifications", NotificationViewSet, basename="notification")

urlpatterns = [path("", include(router.urls)), path("", include(wl_router.urls))]
