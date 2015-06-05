# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from jsonfield import JSONField


SERVICE_OMDB = 'omdb'
SERVICE_CHOICES = (
    (SERVICE_OMDB, 'Open Movie Database'),
    )


@python_2_unicode_compatible
class Movie(models.Model):
    """Minimal amount of data for a Movie."""
    name = models.CharField(max_length=255, db_index=True)
    poster = models.URLField(max_length=255, blank=True, null=True)
    year = models.IntegerField(verbose_name='Year of Release',
                               db_index=True, blank=True, null=True)
    subscribers = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                         through='Watchlist')

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class ServiceMovie(models.Model):
    """Link between a movie and a remote service with more information."""
    movie = models.ForeignKey(Movie)
    service_id = models.CharField(max_length=50, db_index=True)
    service = models.CharField(max_length=10, db_index=True,
                               choices=SERVICE_CHOICES, default=SERVICE_OMDB)
    service_data = JSONField(null=True, blank=True)
    updated = models.DateField(null=True, blank=True, db_index=True)

    class Meta:
        unique_together = ('service_id', 'service')

    def __str__(self):
        return self.movie.name


@python_2_unicode_compatible
class Watchlist(models.Model):
    """
    Link between a movie and a user.
    The Notifications requested are linked to this model.
    """
    movie = models.ForeignKey(Movie)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __str__(self):
        return '{0}/{1}'.format(self.movie.name, self.user.name_or_email)


NOTIFY_CINEMA = 0
NOTIFY_RENTAL = 1
NOTIFY_RETAIL = 2
NOTIFY_STREAMING = 3

NOTIFICATION_CHOICES = (
    (NOTIFY_CINEMA, 'Cinema'),
    (NOTIFY_RETAIL, 'Retail Purchase'),
    )


@python_2_unicode_compatible
class Notification(models.Model):
    """
    A list of the notifications a user has requested.
    """
    watchlist = models.ForeignKey(Watchlist)
    notified = models.BooleanField(default=False)
    notified_date = models.DateField(
        null=True, blank=True,
        help_text='Date when the notification was sent',
        )
    type = models.IntegerField(
        db_index=True,
        choices=NOTIFICATION_CHOICES, default=NOTIFY_CINEMA,
        help_text='Send notification when movie is available for ...'
        )

    class Meta:
        ordering = ('watchlist', 'type')
        unique_together = ('watchlist', 'type')

    def __str__(self):
        return '{0}/{1}/{2}/{3}'.format(
            self.get_type_display(),
            'Y' if self.notified else 'N',
            self.watchlist.movie.name,
            self.watchlist.user.name_or_email,
            )
