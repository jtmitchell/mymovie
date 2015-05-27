# -*- coding: utf-8 -*-
from custom_user.models import AbstractEmailUser
from django.conf import settings
from django.db import models

from django.core.files.storage import get_storage_class

static_storage = get_storage_class(settings.STATICFILES_STORAGE)()


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

    # use the image from social login
    avatar = models.URLField()

    @property
    def avatar_url(self):
        if self.avatar:
            return self.avatar.url
        else:
            return static_storage.url('users/images/avatar-default.png')
