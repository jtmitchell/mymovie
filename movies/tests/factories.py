# -*- coding: utf-8 -*-
import factory
from factory import fuzzy
from faker import Factory as faker

from movies import models
from users.tests.factories import EmailUserFactory


fake = faker.create()


class MovieFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Movie

    name = factory.Sequence(lambda x: 'Movie {0}'.format(x))

    service = factory.RelatedFactory(
        'movies.tests.factories.ServiceMovieFactory',
        'movie',
        )


class ServiceMovieFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.ServiceMovie

    service_id = fake.random_int()
    service = fuzzy.FuzzyChoice([x[0] for x in models.SERVICE_CHOICES])


class WatchlistFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Watchlist

    movie = factory.SubFactory(MovieFactory)
    user = factory.SubFactory(EmailUserFactory)


class NotificationFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Notification

    watchlist = factory.SubFactory(WatchlistFactory)
    type = fuzzy.FuzzyChoice([x[0] for x in models.NOTIFICATION_CHOICES])
