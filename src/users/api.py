from django.shortcuts import get_object_or_404
from ninja import Router

from .models import User
from .schemas import UserOut

router = Router()


@router.get("/me", response=UserOut)
def me(request):
    return request.user


@router.get("/{user_id}", response=UserOut)
def get_user(request, user_id: int):
    return get_object_or_404(
        User.objects.select_related("profile"),  # avoids N+1
        id=user_id,
    )
