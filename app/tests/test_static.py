# -*- coding: utf-8 -*-
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test.client import Client


class TestStatic(StaticLiveServerTestCase):
    """
    Ensure we have the static files we expect.
    """
    def setUp(self):
        self.client = Client()

    def test_robots(self):
        response = self.client.get('/robots.txt', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_favicon(self):
        response = self.client.get('/favicon.ico', follow=True)
        self.assertEqual(response.status_code, 200)
