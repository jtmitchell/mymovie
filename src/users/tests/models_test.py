from django.test import TestCase

from .factories import UserFactory



class TestModels(TestCase):
    """
    Test the database models.
    """

    def test_user_profile(self):
        """
        Ensure a profile is created automatically.
        """
        user = UserFactory()
        self.assertIsNotNone(user.profile, "User profile missing")
        self.assertFalse(user.profile.avatar)
        self.assertEqual(
            user.profile.avatar_url,
            "/users/images/avatar-default.png",
        )
