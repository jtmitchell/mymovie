# flake8: noqa

from unittest.mock import patch
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from movies.models import (
    Watchlist,
    Notification,
    SERVICE_OMDB,
    NOTIFY_CINEMA,
    NOTIFY_RENTAL,
    NOTIFY_STREAMING,
)
from movies.tests.factories import (
    MovieFactory,
    WatchlistFactory,
    NotificationFactory,
)
from users.tests.factories import UserFactory
from users.tests.api_test import TokenTestCase

star_trek_json = {
    "Title": "Star Trek",
    "Year": "2009",
    "Rated": "PG-13",
    "Released": "08 May 2009",
    "Runtime": "127 min",
    "Genre": "Action, Adventure, Sci-Fi",
    "Director": "J.J. Abrams",
    "Writer": "Roberto Orci, Alex Kurtzman, Gene Roddenberry",
    "Actors": "Chris Pine, Zachary Quinto, Simon Pegg",
    "Plot": "The brash James T. Kirk tries to live up to his father's legacy with Mr. Spock keeping him in check as a vengeful Romulan from the future creates black holes to destroy the Federation one planet at a time.",
    "Language": "English",
    "Country": "United States, Germany",
    "Awards": "Won 1 Oscar. 27 wins & 95 nominations total",
    "Poster": "https://m.media-amazon.com/images/M/MV5BMjE5NDQ5OTE4Ml5BMl5BanBnXkFtZTcwOTE3NDIzMw@@._V1_SX300.jpg",
    "Ratings": [
        {"Source": "Internet Movie Database", "Value": "7.9/10"},
        {"Source": "Rotten Tomatoes", "Value": "94%"},
        {"Source": "Metacritic", "Value": "82/100"},
    ],
    "Metascore": "82",
    "imdbRating": "7.9",
    "imdbVotes": "601,303",
    "imdbID": "tt0796366",
    "Type": "movie",
    "DVD": "17 Nov 2009",
    "BoxOffice": "$257,730,019",
    "Production": "N/A",
    "Website": "N/A",
    "Response": "True",
}


class TestMovieApi(TokenTestCase):
    """
    Test the API calls.
    """

    def setUp(self):
        self.client = APIClient(enforce_csrf_checks=True)
        self.user = UserFactory.create()  # suppress @UndefinedVariable
        token = self.create_token(self.user)
        self.auth = f"Bearer {token}"

    def test_get_movie(self):
        movie = MovieFactory.create()  # suppress @UndefinedVariable

        url = reverse("movie-detail", kwargs={"pk": movie.pk})
        response = self.client.get(
            url,
            HTTP_AUTHORIZATION=self.auth,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            f"Got error: {response.content}",
        )

        self.assertEqual(response.data["id"], movie.pk)

    def test_get_watchlist_wrong_user(self):
        watchlist = WatchlistFactory.create()  # suppress @UndefinedVariable

        url = reverse("watchlist-detail", kwargs={"pk": watchlist.pk})
        response = self.client.get(
            url,
            HTTP_AUTHORIZATION=self.auth,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
            f"Got error: {response.content}",
        )

    def test_get_watchlist(self):
        watchlist = WatchlistFactory.create()  # suppress @UndefinedVariable

        url = reverse("watchlist-detail", kwargs={"pk": watchlist.pk})
        response = self.client.get(
            url,
            HTTP_AUTHORIZATION=f"Bearer {self.create_token(watchlist.user)}",
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            f"Got error: {response.content}",
        )

        self.assertEqual(response.data["id"], watchlist.pk)

    def test_create_watchlist(self):
        """
        Create a new watchlist.
        """
        data = dict(
            moviename="Star Trek",
            service=SERVICE_OMDB,
            service_id="tt0796366",
            notifywhen=[NOTIFY_CINEMA, NOTIFY_RENTAL, NOTIFY_STREAMING],
        )
        url = reverse("watchlist-list")

        with patch("movies.models.omdb.get") as mock:
            mock.return_value = star_trek_json
            response = self.client.post(
                url,
                data=data,
                HTTP_AUTHORIZATION=self.auth,
                format="json",
            )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
            f"Got error: {response.content}",
        )

        self.assertIn("id", response.data, "Missing id")
        self.assertIn("movie", response.data, "Missing movie")
        self.assertIn("notifications", response.data, "Missing notifications")

    def test_delete_watchlist(self):
        watchlist = WatchlistFactory.create()  # suppress @UndefinedVariable

        url = reverse("watchlist-detail", kwargs={"pk": watchlist.pk})
        response = self.client.delete(
            url,
            HTTP_AUTHORIZATION=f"Bearer {self.create_token(watchlist.user)}",
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
            f"Got error: {response.content}",
        )
        self.assertQuerysetEqual(
            Watchlist.objects.filter(pk=watchlist.pk),
            [],
            "Deleted watchlist is in database",
        )

    def test_delete_watchlist_wrong_user(self):
        watchlist = WatchlistFactory.create()  # suppress @UndefinedVariable

        url = reverse("watchlist-detail", kwargs={"pk": watchlist.pk})
        response = self.client.delete(
            url,
            HTTP_AUTHORIZATION=self.auth,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
            f"Got error: {response.content}",
        )

    def test_get_notification(self):
        notify = NotificationFactory.create()  # suppress @UndefinedVariable

        url = reverse("notification-detail", args=[notify.watchlist.pk, notify.pk])
        response = self.client.get(
            url,
            HTTP_AUTHORIZATION=f"Bearer {self.create_token(notify.watchlist.user)}",
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            f"Got error: {response.content}",
        )

        self.assertEqual(response.data["id"], notify.pk)

    def test_get_notification_wrong_user(self):
        notify = NotificationFactory.create()  # suppress @UndefinedVariable

        url = reverse("notification-detail", args=[notify.watchlist.pk, notify.pk])
        response = self.client.get(
            url,
            HTTP_AUTHORIZATION=self.auth,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
            f"Got error: {response.content}",
        )

    def test_delete_notification(self):
        notify = NotificationFactory.create()  # suppress @UndefinedVariable

        url = reverse("notification-detail", args=[notify.watchlist.pk, notify.pk])
        response = self.client.delete(
            url,
            HTTP_AUTHORIZATION=f"Bearer {self.create_token(notify.watchlist.user)}",
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
            f"Got error: {response.content}",
        )
        self.assertQuerysetEqual(
            Notification.objects.filter(pk=notify.pk),
            [],
            "Deleted notification is in database",
        )
