from custom_user.admin import EmailUserAdmin
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from utils.actions import export_as_csv_action

from .models import UserProfile, EmailUser


class UserProfileInline(admin.StackedInline):
    model = UserProfile


class UserAdmin(EmailUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Details'), {'fields': ('name',)}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
    )

    list_display = ('email', 'name', 'is_staff', 'last_login')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email', 'name',)
    inlines = (UserProfileInline,)
    actions = [
        export_as_csv_action(
            "Export selection to CSV file",
            fields=list_display, header=True, force_fields=True
            ),
        ]

admin.site.register(EmailUser, UserAdmin)
