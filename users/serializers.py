from rest_framework import serializers

from .models import EmailUser


class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.URLField(read_only=True, source='profile.avatar_url')

    class Meta:
        model = EmailUser
        fields = ('id', 'email', 'name', 'avatar')
