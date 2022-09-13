from rest_framework import serializers
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.URLField(read_only=True, source="profile.avatar_url")
    full_name = serializers.CharField(read_only=True, source="get_full_name")

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "full_name",
            "avatar",
        )
