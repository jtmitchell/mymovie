# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.files.storage import get_storage_class
from django.test import TestCase

from .factories import UserFactory


static_storage = get_storage_class(settings.STATICFILES_STORAGE)()


class TestModels(TestCase):
    """
    Test the database models.
    """
    def test_user_profile(self):
        """Ensure a profile is created automatically."""
        user = UserFactory()
        self.assertIsNotNone(user.profile, 'User profile missing')
        self.assertFalse(user.profile.avatar)
        self.assertEqual(user.profile.avatar_url,
                         static_storage.url('users/images/avatar-default.png'),
                         )
