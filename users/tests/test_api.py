# -*- coding: utf-8 -*-
from calendar import timegm

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_jwt import utils

from .factories import UserFactory
from django.contrib.auth import get_user_model


class TokenTestCase(TestCase):
    """
    Methods from the JWT tests to work with tokens.
    """
    def create_token(self, user, exp=None, orig_iat=None):
        payload = utils.jwt_payload_handler(user)
        if exp:
            payload['exp'] = exp

        if orig_iat:
            payload['orig_iat'] = timegm(orig_iat.utctimetuple())

        token = utils.jwt_encode_handler(payload)
        return token


class TestUserApi(TokenTestCase):
    """
    Test the API calls.
    """
    def setUp(self):
        self.client = APIClient(enforce_csrf_checks=True)

    def test_login(self):
        """Test the login endpoint"""
        user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@test.domain.com',
            password='password',
            )

        data = dict(
            username=user.username,
            email=user.email,
            password='password',
            )

        response = self.client.post(
            '/api/v1/auth/login',
            data=data,
            format='json',
            )

        self.assertEqual(response.status_code, status.HTTP_200_OK,
                         'Got error: {}'.format(response.content))

        decoded_payload = utils.jwt_decode_handler(response.data['token'])

        self.assertEqual(decoded_payload['username'], user.username)
        self.assertEqual(decoded_payload['email'], user.email)
        self.assertEqual(decoded_payload['user_id'], user.pk)

    def test_get_info(self):
        """Call the get info endpoint"""
        user = UserFactory.create()  # suppress @UndefinedVariable

        auth = 'JWT {}'.format(self.create_token(user))

        response = self.client.get(
            '/api/v1/users/me',
            HTTP_AUTHORIZATION=auth,
            format='json',
            )

        self.assertEqual(response.status_code, status.HTTP_200_OK,
                         'Got error: {}'.format(response.content))

        self.assertEqual(response.data['email'], user.email)
        self.assertEqual(response.data['id'], user.pk)
        self.assertEqual(response.data['first_name'], user.first_name)
        self.assertEqual(response.data['last_name'], user.last_name)
        self.assertEqual(response.data['full_name'], user.get_full_name())
        self.assertEqual(response.data['avatar'], user.profile.avatar_url)
