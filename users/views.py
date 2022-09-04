# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.views.decorators.cache import never_cache
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()

    @never_cache
    @action(detail=False)
    def me(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)
