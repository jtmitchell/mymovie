# -*- coding: utf-8 -*-
from faker import Factory as faker
import factory
from django.contrib.auth import get_user_model

fake = faker.create()

TEST_PASSWORD = 'password'


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = fake.profile()['username']
    email = fake.email()
    password = TEST_PASSWORD
    first_name = fake.first_name()
    last_name = fake.last_name()
