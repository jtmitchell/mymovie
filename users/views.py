# -*- coding: utf-8 -*-
from .models import EmailUser
from .serializers import UserSerializer
from django.views.decorators.cache import never_cache
from custom_rest_framework.viewsets import JWTViewSet
from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response


class UserViewSet(JWTViewSet, viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = EmailUser.objects.all()

    @never_cache
    @list_route()
    def me(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)
