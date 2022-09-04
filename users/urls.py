# -*- coding: utf-8 -*-
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
router.register("v1/users", UserViewSet, basename="user")

auth_patterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]

urlpatterns = [
    path("", include(router.urls)),
    path("v1/auth/", include(auth_patterns)),
]
