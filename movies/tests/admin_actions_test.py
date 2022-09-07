from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase, Client

from .factories import MovieFactory


class TestMovieAdminActions(TestCase):
    """
    Test custom admin actions.

    - export to csv

    """

    def setUp(self):
        User = get_user_model()
        self.client = Client()
        self.superuser = User.objects.create_superuser(
            username="test", email="test@test.co.nz", password="test"
        )
        self.client.post(
            reverse("admin:login"),
            data=dict(username=self.superuser.username, password="test"),
            follow=False,
        )

    def test_export_csv(self):
        """
        Export CSV action for movies.
        """
        MovieFactory.create()  # suppress @UndefinedVariable

        data = dict(
            _selected_action=["1"],
            action=["export_as_csv"],
            index=["0"],
            select_across=["0"],
        )
        response = self.client.post(
            reverse("admin:movies_movie_changelist"), data=data, follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.has_header("content-type"))
        self.assertEqual(
            response.headers.get("content-type"),
            "text/csv",
        )
