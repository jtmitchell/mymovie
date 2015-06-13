# -*- coding: utf-8 -*-
from rest_framework import viewsets

from custom_rest_framework.viewsets import JWTViewSet

from .models import Movie, Watchlist, Notification
from .serializers import MovieSerializer, \
    WatchlistSerializer, \
    NotificationSerializer


class MovieViewSet(JWTViewSet, viewsets.ModelViewSet):
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()


class WatchlistViewSet(JWTViewSet, viewsets.ModelViewSet):
    serializer_class = WatchlistSerializer

    def get_queryset(self):
        """Filter based on the auth user"""
        user = self.request.user
        return Watchlist.objects.filter(user=user)


class NotificationViewSet(JWTViewSet, viewsets.ModelViewSet):
    serializer_class = NotificationSerializer

    def get_queryset(self):
        """Filter based on the auth user"""
        user = self.request.user
        return Notification.objects.filter(watchlist__user=user)
