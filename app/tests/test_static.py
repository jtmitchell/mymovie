# -*- coding: utf-8 -*-
import os

from django.urls import reverse
from django.contrib.staticfiles import finders
from django.test import TestCase, Client


class TestStatic(TestCase):
    """
    Ensure we have the static files we expect.
    """

    def setUp(self):
        self.client = Client()

    def test_robots(self):
        file_path = finders.find("app/robots.txt")
        self.assertIsNotNone(file_path, "Failed to find robots.txt")
        self.assertTrue(os.path.exists(file_path))

        # test the redirection
        response = self.client.get(reverse("robots"), follow=False)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            "/static/app/robots.txt",
        )

    def test_favicon(self):
        file_path = finders.find("app/favicon.png")
        self.assertIsNotNone(file_path, "Failed to find favicon.png")
        self.assertTrue(os.path.exists(file_path))

        # test the redirection
        response = self.client.get(reverse("favicon"), follow=False)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            "/static/app/favicon.png",
        )


class TestHomepage(TestCase):
    """
    Load the homepage.
    """

    def setUp(self):
        self.client = Client()

    def test_homepage(self):
        response = self.client.get(reverse("homepage"), follow=False)
        self.assertEqual(response.status_code, 200)
