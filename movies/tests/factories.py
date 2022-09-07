import datetime
import factory

from factory.django import DjangoModelFactory
from factory import fuzzy
from faker import Faker

from movies import models
from users.tests.factories import UserFactory


fake = Faker()


class MovieFactory(DjangoModelFactory):
    class Meta:
        model = models.Movie

    name = factory.Sequence(lambda x: f"Movie {x}")
    poster = fake.url()
    year = fuzzy.FuzzyDate(datetime.date(2015, 1, 1)).fuzz().year
    service = factory.RelatedFactory(
        "movies.tests.factories.ServiceMovieFactory",
        "movie",
    )


class ServiceMovieFactory(DjangoModelFactory):
    class Meta:
        model = models.ServiceMovie

    service_id = fake.random_int()
    service = fuzzy.FuzzyChoice([x[0] for x in models.SERVICE_CHOICES])
    service_data = dict(jsonfield="Sample data")
    updated = fuzzy.FuzzyDate(datetime.date(2015, 1, 1))


class WatchlistFactory(DjangoModelFactory):
    class Meta:
        model = models.Watchlist

    movie = factory.SubFactory(MovieFactory)
    user = factory.SubFactory(UserFactory)


class NotificationFactory(DjangoModelFactory):
    class Meta:
        model = models.Notification

    watchlist = factory.SubFactory(WatchlistFactory)
    type = fuzzy.FuzzyChoice([x[0] for x in models.NOTIFICATION_CHOICES])
