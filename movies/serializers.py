# -*- coding: utf-8 -*-
from rest_framework import serializers

from .models import Movie, Watchlist, Notification


class MovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie


class WatchlistSerializer(serializers.ModelSerializer):

    class Meta:
        model = Watchlist


class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
