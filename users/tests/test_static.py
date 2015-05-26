# -*- coding: utf-8 -*-
import os

from django.contrib.staticfiles import finders
from django.test import TestCase, Client


class TestStatic(TestCase):
    """
    Ensure we have the default avatar image.
    """
    def setUp(self):
        self.client = Client()

    def test_default_avatar(self):
        file_path = finders.find('users/images/avatar-default.png')
        self.assertIsNotNone(file_path, 'Failed to find avatar-default.png')
        self.assertTrue(os.path.exists(file_path))
