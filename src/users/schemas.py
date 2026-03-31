from ninja import ModelSchema

from .models import User, UserProfile


class UserProfileOut(ModelSchema):
    class Meta:
        model = UserProfile
        fields = ["avatar"]


class UserOut(ModelSchema):
    profile: UserProfileOut | None = None

    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name"]
