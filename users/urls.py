# -*- coding: utf-8 -*-
"""
Urls for the user models.
"""
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from .views import UserViewSet

router = DefaultRouter(trailing_slash=False)
router.include_format_suffixes = False
router.register("users", UserViewSet, basename="user")

auth_patterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]

urlpatterns = [
    path("", include(router.urls)),
    path("auth/", include(auth_patterns)),
]
