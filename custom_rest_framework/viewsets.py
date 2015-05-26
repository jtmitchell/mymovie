# -*- coding: utf-8 -*-
from calendar import timegm
from datetime import datetime

from django.conf import settings
from rest_framework import generics
from rest_framework_jwt.utils import jwt_decode_handler


class JWTViewSet(generics.GenericAPIView):
    def finalize_response(self, request, response, *args, **kwargs):
        """
        Add a response header to suggest a token refresh
        when we get close to the expiration time.
        """
        response = super(JWTViewSet, self).finalize_response(
            request,
            response,
            *args, **kwargs
            )
        auth = request.auth
        delta = settings.JWT_SUGGEST_REFRESH_DELTA
        if auth:
            try:
                payload = jwt_decode_handler(auth)
                expiry = payload.get('exp')
                utc_timestamp = timegm(datetime.utcnow().utctimetuple())
                if utc_timestamp > (expiry - delta.seconds):
                    response['Suggest-Token-Refresh'] = 'True'
            except:
                # the token has expired, so no need to try and refresh it
                pass

        return response
