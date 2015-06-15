# -*- coding: utf-8 -*-
import datetime

from factory import fuzzy
import factory
from faker import Factory as faker

from movies import models
from users.tests.factories import UserFactory


fake = faker.create()


class MovieFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Movie

    name = factory.Sequence(lambda x: 'Movie {0}'.format(x))
    poster = fake.url()
    year = fuzzy.FuzzyDate(datetime.date(2015, 1, 1)).fuzz().year
    service = factory.RelatedFactory(
        'movies.tests.factories.ServiceMovieFactory',
        'movie',
        )


class ServiceMovieFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.ServiceMovie

    service_id = fake.random_int()
    service = fuzzy.FuzzyChoice([x[0] for x in models.SERVICE_CHOICES])
    service_data = dict(jsonfield='Sample data')
    updated = fuzzy.FuzzyDate(datetime.date(2015, 1, 1))


class WatchlistFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Watchlist

    movie = factory.SubFactory(MovieFactory)
    user = factory.SubFactory(UserFactory)


class NotificationFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Notification

    watchlist = factory.SubFactory(WatchlistFactory)
    type = fuzzy.FuzzyChoice([x[0] for x in models.NOTIFICATION_CHOICES])


class WatchlistWithNotificationsFactory(WatchlistFactory):
    notify1 = factory.RelatedFactory(
        NotificationFactory,
        'watchlist',
        type=models.NOTIFICATION_CHOICES[0][0])
    notify2 = factory.RelatedFactory(
        NotificationFactory,
        'watchlist',
        type=models.NOTIFICATION_CHOICES[1][0])
