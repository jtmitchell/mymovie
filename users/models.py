# -*- coding: utf-8 -*-
from custom_user.models import AbstractEmailUser
from django.conf import settings
from django.db import models


class EmailUser(AbstractEmailUser):
    name = models.CharField('Name', max_length=255, blank=True, null=True)

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def save(self, *args, **kwargs):
        super(EmailUser, self).save(*args, **kwargs)
        try:
            profile = self.profile
        except UserProfile.DoesNotExist:
            profile = UserProfile(user=self)
            profile.save()
            self.profile = profile


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name='profile'
        )
    avatar = models.URLField()  # use the image from social login
