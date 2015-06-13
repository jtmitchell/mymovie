# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APIClient

from movies.tests.factories import MovieFactory, WatchlistFactory, \
    NotificationFactory
from users.tests.factories import UserFactory
from users.tests.test_api import TokenTestCase


class TestMovieApi(TokenTestCase):
    """
    Test the API calls.
    """
    def setUp(self):
        self.client = APIClient(enforce_csrf_checks=True)
        self.user = UserFactory.create()  # suppress @UndefinedVariable
        self.auth = 'JWT {}'.format(self.create_token(self.user))

    def test_get_movie(self):
        movie = MovieFactory.create()  # suppress @UndefinedVariable

        response = self.client.get(
            '/api/v1/movies/{}'.format(movie.pk),
            HTTP_AUTHORIZATION=self.auth,
            format='json',
            )

        self.assertEqual(response.status_code, status.HTTP_200_OK,
                         'Got error: {}'.format(response.content))

        self.assertEqual(response.data['id'], movie.pk)

    def test_get_watchlist_wrong_user(self):
        watchlist = WatchlistFactory.create()  # suppress @UndefinedVariable

        response = self.client.get(
            '/api/v1/watchlists/{}'.format(watchlist.pk),
            HTTP_AUTHORIZATION=self.auth,
            format='json',
            )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND,
                         'Got error: {}'.format(response.content))

    def test_get_watchlist(self):
        watchlist = WatchlistFactory.create()  # suppress @UndefinedVariable

        response = self.client.get(
            '/api/v1/watchlists/{}'.format(watchlist.pk),
            HTTP_AUTHORIZATION='JWT {}'.format(
                self.create_token(watchlist.user)
                ),
            format='json',
            )

        self.assertEqual(response.status_code, status.HTTP_200_OK,
                         'Got error: {}'.format(response.content))

        self.assertEqual(response.data['id'], watchlist.pk)

    def test_get_notification(self):
        notify = NotificationFactory.create()  # suppress @UndefinedVariable

        response = self.client.get(
            '/api/v1/watchlists/{}/notifications/{}'.format(
                notify.watchlist.pk,
                notify.pk,
                ),
            HTTP_AUTHORIZATION='JWT {}'.format(
                self.create_token(notify.watchlist.user)
                ),
            format='json',
            )

        self.assertEqual(response.status_code, status.HTTP_200_OK,
                         'Got error: {}'.format(response.content))

        self.assertEqual(response.data['id'], notify.pk)

    def test_get_notification_wrong_user(self):
        notification = NotificationFactory.create()  # suppress @UndefinedVariable

        response = self.client.get(
            '/api/v1/watchlists/{}/notifications/{}'.format(
                notification.watchlist.pk,
                notification.pk,
                ),
            HTTP_AUTHORIZATION=self.auth,
            format='json',
            )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND,
                         'Got error: {}'.format(response.content))
