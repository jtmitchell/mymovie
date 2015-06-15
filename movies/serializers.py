# -*- coding: utf-8 -*-
from rest_framework import serializers

from .models import Movie, Watchlist, Notification, ServiceMovie


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceMovie
        fields = ('id', 'service', 'service_id', 'updated', 'service_data')


class MovieSerializer(serializers.ModelSerializer):
    services = ServiceSerializer(many=True, source='servicemovie_set')

    class Meta:
        model = Movie
        fields = ('id', 'name', 'poster', 'year', 'services')


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification


class WatchlistSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)
    notifications = NotificationSerializer(
        read_only=True,
        many=True,
        source='notification_set')

    class Meta:
        model = Watchlist
