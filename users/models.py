# -*- coding: utf-8 -*-
from custom_user.models import AbstractEmailUser
from django.conf import settings
from django.db import models

from django.core.files.storage import get_storage_class
from django.utils.encoding import python_2_unicode_compatible

static_storage = get_storage_class(settings.STATICFILES_STORAGE)()


@python_2_unicode_compatible
class EmailUser(AbstractEmailUser):
    name = models.CharField('Name', max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name_or_email

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    @property
    def name_or_email(self):
        return self.name if self.name else self.email

    def save(self, *args, **kwargs):
        super(EmailUser, self).save(*args, **kwargs)
        try:
            profile = self.profile
        except UserProfile.DoesNotExist:
            profile = UserProfile(user=self)
            profile.save()
            self.profile = profile


@python_2_unicode_compatible
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
            return self.avatar
        else:
            return static_storage.url('users/images/avatar-default.png')

    def __str__(self):
        return self.user.name_or_email
