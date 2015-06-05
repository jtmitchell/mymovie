# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import UserProfile
from django.contrib.auth import get_user_model


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False


class UserAdmin(UserAdmin):
    inlines = (UserProfileInline,)

admin.site.unregister(get_user_model())
admin.site.register(get_user_model(), UserAdmin)
