from django.conf import settings
from django.core.files.storage import get_storage_class
from django.db import models
from django.db.models.signals import post_save


static_storage = get_storage_class(settings.STATICFILES_STORAGE)()


class UserProfile(models.Model):
    """
    Profile to store additional user data.
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name="profile",
        on_delete=models.CASCADE,
    )

    # use the image from social login
    avatar = models.URLField()

    @property
    def avatar_url(self):
        """
        Return the url to the avatar image.
        """
        if self.avatar:
            return self.avatar
        return static_storage.url("users/images/avatar-default.png")

    def __str__(self):
        return self.user.get_full_name()


def post_save_profile(sender, instance, created, **kwargs):
    """
    Save the profile data.
    """
    try:
        profile = instance.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile(user=instance)
        profile.save()
        instance.profile = profile


post_save.connect(
    post_save_profile,
    sender=settings.AUTH_USER_MODEL,
)
