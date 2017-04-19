# -*- coding: utf-8 -*-
from calendar import timegm
from datetime import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.views.decorators.cache import never_cache
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.decorators import list_route
from rest_framework.exceptions import PermissionDenied, AuthenticationFailed
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from social_django.utils import psa

from custom_rest_framework.viewsets import JWTViewSet

from .serializers import UserSerializer


class UserViewSet(JWTViewSet, viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()

    @never_cache
    @list_route()
    def me(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)


jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


@psa('social:complete')
@api_view(http_method_names=['GET'])
@permission_classes([AllowAny])
def obtain_token_view(request, *args, **kwargs):
    token = request.GET.get('access_token')
    user = request.backend.do_auth(token)
    if user:
        if not user.is_active:
            msg = 'User account is disabled.'
            raise PermissionDenied(msg)

        login(request, user)  # is this needed? sets last login time?
        payload = jwt_payload_handler(user)

        # Include original issued at time for a brand new token,
        # to allow token refresh
        if api_settings.JWT_ALLOW_REFRESH:
            payload['orig_iat'] = timegm(
                datetime.utcnow().utctimetuple()
            )

        return Response(
            dict(
                token=jwt_encode_handler(payload),
                user=dict(
                    id=user.pk,
                    email=user.email,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    name=user.get_full_name(),
                    avatar=user.profile.avatar_url,
                    is_staff=user.is_staff,
                    last_login=user.last_login,
                    ),
                )
            )
    else:
        msg = 'Unable to login with provided credentials.'
        raise AuthenticationFailed(msg)
