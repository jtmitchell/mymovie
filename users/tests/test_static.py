# -*- coding: utf-8 -*-
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test.client import Client


class TestStatic(StaticLiveServerTestCase):
    """
    Ensure we have the default avatar image.
    """
    def setUp(self):
        self.client = Client()

    def test_default_avatar(self):
        response = self.client.get('/static/users/images/avatar-default.png')
        self.assertEqual(response.status_code, 200)
