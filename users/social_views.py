# -*- coding: utf-8 -*-

# This is a separate views file so we can lazy load the social imports

from calendar import timegm
from datetime import datetime

from django.contrib.auth import login
from django.core.urlresolvers import reverse
from django.http.response import Http404
from rest_framework.exceptions import PermissionDenied, AuthenticationFailed
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings
from social.apps.django_app.utils import load_strategy, load_backend
from social.exceptions import MissingBackend


jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class ObtainTokenView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, backend, *args, **kwargs):
        """
        This view expects an access_token GET parameter, if it's needed,
        request.backend and request.strategy will be loaded with the current
        backend and strategy.

        Had to also pull in code from the @psa decorator
        From the Python Social Auth docs.
        """
        uri = reverse('social:complete', args=(backend,))
        request.social_strategy = load_strategy(request)
        # backward compatibility in attribute name, only if not already
        # defined
        if not hasattr(request, 'strategy'):
            request.strategy = request.social_strategy

        try:
            request.backend = load_backend(request.social_strategy,
                                           backend, uri)
        except MissingBackend:
            raise Http404('Backend not found')

        token = request.DATA.get('access_token')
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
                    user=user,
                    )
                )
        else:
            msg = 'Unable to login with provided credentials.'
            raise AuthenticationFailed(msg)

obtain_token_view = ObtainTokenView.as_view()
