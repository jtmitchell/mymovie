from rest_framework import serializers

from .models import EmailUser
from django.core.files.storage import get_storage_class
from django.conf import settings

static_storage = get_storage_class(settings.STATICFILES_STORAGE)()


class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField('avatar_or_default')

    class Meta:
        model = EmailUser
        fields = ('id', 'email', 'name', 'avatar')

    def avatar_or_default(self, obj):
        if obj.profile and obj.profile.avatar:
            return obj.profile.avatar.url
        else:
            return static_storage.url('users/images/avatar-default.png')
