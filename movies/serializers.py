from rest_framework import serializers

from .models import Movie, Watchlist, Notification, ServiceMovie
from users.serializers import UserSerializer


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceMovie
        fields = ("id", "service", "service_id", "updated", "service_data")


class MovieSerializer(serializers.ModelSerializer):
    services = ServiceSerializer(many=True, source="servicemovie_set")

    class Meta:
        model = Movie
        fields = ("id", "name", "poster", "year", "services")


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"


class WatchlistSerializer(serializers.ModelSerializer):
    user = UserSerializer(write_only=True, required=False)
    movie = MovieSerializer(read_only=True)
    notifications = NotificationSerializer(
        read_only=True, many=True, source="notification_set"
    )

    # fields used when creating a new watchlist
    moviename = serializers.CharField(write_only=True)
    notifywhen = serializers.ListField(write_only=True)
    service = serializers.CharField(write_only=True)
    service_id = serializers.CharField(write_only=True)

    class Meta:
        model = Watchlist
        fields = "__all__"

    def create(self, validated_data):
        """
        Save the new watchlist and associated notifications and movies.
        """
        ModelClass = self.Meta.model

        moviename = validated_data.pop("moviename")
        notifywhen = validated_data.pop("notifywhen")
        service = validated_data.pop("service")
        service_id = validated_data.pop("service_id")

        movie = Movie.objects.lookup(
            name=moviename,
            service=service,
            service_id=service_id,
        )

        validated_data.update(dict(movie=movie))

        try:
            instance = ModelClass.objects.create(**validated_data)
        except TypeError as exc:
            msg = (
                f"Got a `TypeError` when calling `{ModelClass.__name__}.objects.create()`. "
                "This may be because you have a writable field on the serializer class "
                f"that is not a valid argument to `{ModelClass.__name__}.objects.create()`. "
                "You may need to make the field read-only, "
                f"or override the {self.__class__.__name__}.create() method to handle "
                "this correctly.\n"
                f"Original exception text was: {exc}."
            )
            raise TypeError(msg)

        for notify_type in notifywhen:
            Notification.objects.create(watchlist=instance, type=notify_type)

        return instance
