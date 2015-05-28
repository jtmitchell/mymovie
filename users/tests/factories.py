# -*- coding: utf-8 -*-
from faker import Factory as faker
import factory
from users import models

fake = faker.create()

TEST_PASSWORD = 'password'


class EmailUserFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.EmailUser

    email = fake.email()
    password = TEST_PASSWORD
    name = fake.name()
