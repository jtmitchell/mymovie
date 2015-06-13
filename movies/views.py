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
    queryset = Watchlist.objects.all()


class NotificationViewSet(JWTViewSet, viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()
