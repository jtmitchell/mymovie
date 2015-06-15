# -*- coding: utf-8 -*-
import json
import os

from django.contrib.staticfiles import finders
from django.test import TestCase, Client

TESTSERVER = 'http://testserver'


class TestStatic(TestCase):
    """
    Ensure we have the static files we expect.
    """
    def setUp(self):
        self.client = Client()

    def test_robots(self):
        file_path = finders.find('app/robots.txt')
        self.assertIsNotNone(file_path, 'Failed to find robots.txt')
        self.assertTrue(os.path.exists(file_path))

        # test the redirection
        response = self.client.get('/robots.txt', follow=False)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            '{0}/static/{1}'.format(TESTSERVER, 'app/robots.txt'),
            )

    def test_favicon(self):
        file_path = finders.find('app/favicon.png')
        self.assertIsNotNone(file_path, 'Failed to find favicon.png')
        self.assertTrue(os.path.exists(file_path))

        # test the redirection
        response = self.client.get('/favicon.ico', follow=False)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            '{0}/static/{1}'.format(TESTSERVER, 'app/favicon.png'),
            )


class TestHomepage(TestCase):
    """Load the homepage"""
    def setUp(self):
        self.client = Client()

    def test_homepage(self):
        response = self.client.get('/', follow=False)
        self.assertEqual(response.status_code, 200)
