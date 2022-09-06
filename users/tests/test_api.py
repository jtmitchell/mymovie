# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from mock import patch
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from .factories import UserFactory


class TokenTestCase(TestCase):
    """
    Methods from the JWT tests to work with tokens.
    """

    def create_token(self, user):
        refresh = RefreshToken.for_user(user)
        return refresh.access_token


class TestUserApi(TokenTestCase):
    """
    Test the API calls.
    """

    def setUp(self):
        self.client = APIClient(enforce_csrf_checks=True)

    def test_login(self):
        """
        Test the login endpoint.
        """
        user = get_user_model().objects.create_user(
            username="testuser",
            email="testuser@test.domain.com",
            password="password",
        )

        data = dict(
            username=user.username,
            email=user.email,
            password="password",
        )

        response = self.client.post(
            reverse("token_obtain_pair"),  # "/api/v1/auth/token",
            data=data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            f"Got error: {response.content}",
        )

    def test_get_info(self):
        """
        Call the get info endpoint.
        """
        user = UserFactory.create()  # suppress @UndefinedVariable

        headers = {"HTTP_AUTHORIZATION": f"Bearer {self.create_token(user)}"}
        url = reverse("user-me")
        response = self.client.get(
            url,
            format="json",
            **headers,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            f"Got error: {response.content}",
        )

        self.assertEqual(response.data["email"], user.email)
        self.assertEqual(response.data["id"], user.pk)
        self.assertEqual(response.data["first_name"], user.first_name)
        self.assertEqual(response.data["last_name"], user.last_name)
        self.assertEqual(response.data["full_name"], user.get_full_name())
        self.assertEqual(response.data["avatar"], user.profile.avatar_url)
