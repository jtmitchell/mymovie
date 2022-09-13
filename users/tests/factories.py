import factory

from factory.django import DjangoModelFactory
from faker import Faker
from django.contrib.auth import get_user_model

fake = Faker()

TEST_PASSWORD = "password"


class UserFactory(DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = factory.Sequence(lambda n: f"user{n}")
    email = fake.email()
    password = TEST_PASSWORD
    first_name = fake.first_name()
    last_name = fake.last_name()
