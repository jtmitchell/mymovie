# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from rest_framework.routers import DefaultRouter

from .views import UserViewSet

router = DefaultRouter(trailing_slash=False)
router.include_format_suffixes = False
router.register(r'v1/users', UserViewSet, base_name='user')

auth_patterns = patterns('',
                         url(r'^login/$', 'rest_framework_jwt.views.obtain_jwt_token', name="login"),
                         url(r'^token-refresh/$', 'rest_framework_jwt.views.refresh_jwt_token', name='token_refresh'),
                         )

urlpatterns = patterns('',
                       url(r'', include(router.urls, namespace='users')),
                       url(r'^v1/auth/', include(auth_patterns, namespace='auth')),
                       )
