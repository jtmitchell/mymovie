# -*- coding: utf-8 -*-
import datetime

from django.conf import settings
from django.db import models
from jsonfield import JSONField

from movies.service import omdb


SERVICE_OMDB = "omdb"
SERVICE_CHOICES = ((SERVICE_OMDB, "Open Movie Database"),)


class MovieManager(models.Manager):
    def lookup(self, name=None, service=SERVICE_OMDB, service_id=None):
        """
        Lookup a movie.

        If we don't have it already, retrieve data from the service.

        """
        movie = None
        qs = self.filter(
            servicemovie__service=service, servicemovie__service_id=service_id
        )

        if qs.exists():
            return qs[0]
        else:
            movie_data = omdb.get(service_id=service_id)

            if movie_data:
                movie, _ = self.get_or_create(
                    name=movie_data.get("Title", name),
                    year=movie_data.get("Year"),
                    poster=movie_data.get("Poster"),
                )

                service, _ = ServiceMovie.objects.get_or_create(
                    movie=movie,
                    service=service,
                    service_id=service_id,
                )
                service.service_data = movie_data
                service.updated = datetime.date.today()
                service.save()

        return movie


class Movie(models.Model):
    """
    Minimal amount of data for a Movie.
    """

    name = models.CharField(max_length=255, db_index=True)
    poster = models.URLField(max_length=255, blank=True, null=True)
    year = models.CharField(
        max_length=20,
        verbose_name="Year of Release",
        db_index=True,
        blank=True,
        null=True,
    )
    subscribers = models.ManyToManyField(settings.AUTH_USER_MODEL, through="Watchlist")

    objects = MovieManager()

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return f"{self.name}"


class ServiceMovie(models.Model):
    """
    Link between a movie and a remote service with more information.
    """

    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    service_id = models.CharField(max_length=50, db_index=True)
    service = models.CharField(
        max_length=10, db_index=True, choices=SERVICE_CHOICES, default=SERVICE_OMDB
    )
    service_data = JSONField(null=True, blank=True)
    updated = models.DateField(null=True, blank=True, db_index=True)

    class Meta:
        unique_together = ("service_id", "service")

    def __str__(self):
        return f"{self.movie.name}"


class Watchlist(models.Model):
    """
    Link between a movie and a user.

    The Notifications requested are linked to this model.

    """

    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.movie.name}/{self.user.get_full_name()}"


NOTIFY_CINEMA = 0
NOTIFY_RETAIL = 1
NOTIFY_RENTAL = 2
NOTIFY_STREAMING = 3

NOTIFICATION_CHOICES = (
    (NOTIFY_CINEMA, "Cinema"),
    (NOTIFY_RETAIL, "Retail Purchase"),
    (NOTIFY_RENTAL, "Rental"),
    (NOTIFY_STREAMING, "Online Streaming"),
)


class Notification(models.Model):
    """
    A list of the notifications a user has requested.
    """

    watchlist = models.ForeignKey(Watchlist, on_delete=models.CASCADE)
    notified = models.BooleanField(default=False)
    notified_date = models.DateField(
        null=True,
        blank=True,
        help_text="Date when the notification was sent",
    )
    type = models.IntegerField(
        db_index=True,
        choices=NOTIFICATION_CHOICES,
        default=NOTIFY_CINEMA,
        help_text="Send notification when movie is available for ...",
    )

    class Meta:
        ordering = ("watchlist", "type")
        unique_together = ("watchlist", "type")

    def __str__(self):
        return "{0}/{1}/{2}/{3}".format(
            self.get_type_display(),
            "Y" if self.notified else "N",
            self.watchlist.movie.name,
            self.watchlist.user.get_full_name(),
        )
