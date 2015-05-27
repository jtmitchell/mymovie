# -*- coding: utf-8 -*-
from faker import Factory as faker
import factory
from users import models

fake = faker.create()


class EmailUserFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.EmailUser

    email = fake.email()
    name = fake.name()
