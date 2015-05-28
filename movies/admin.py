from django.contrib import admin

from movies.models import ServiceMovie, Movie, Notification, Watchlist
from utils.actions import export_as_csv_action


class ExtraOnNew(object):
    """Mixin to not put extra blank rows in."""
    def get_extra(self, request, obj=None, **kwargs):
        if obj:
            # Don't add any extra forms if the related object already exists.
            return 0
        return self.extra


class ServiceMovie_Inline(ExtraOnNew, admin.StackedInline):
    model = ServiceMovie
    extra = 1


class MovieAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    inlines = (ServiceMovie_Inline,)
    actions = [
        export_as_csv_action(
            "Export selection to CSV file",
            fields=list_display, header=True, force_fields=True
            ),
        ]


class Notification_Inline(ExtraOnNew, admin.StackedInline):
    model = Notification
    extra = 2


class WatchlistAdmin(admin.ModelAdmin):
    def watchlist_movie_name(self, obj):
        return obj.movie.name

    def watchlist_user_name(self, obj):
        return obj.user.name

    def notifications(self, obj):
        notifications = []
        for item in obj.notification_set.all():
            notifications.append('{0}/{1}'.format(
                item.get_type_display(),
                'Y' if item.notified else 'N',
                ))
        return ' '.join(notifications)

    list_display = ('watchlist_movie_name', 'watchlist_user_name', 'notifications')
    search_fields = ('movie__name', 'user__name', 'user__email')
    inlines = (Notification_Inline,)
    actions = [
        export_as_csv_action(
            "Export selection to CSV file",
            fields=list_display, header=True, force_fields=True
            ),
        ]

admin.site.register(Movie, MovieAdmin)
admin.site.register(Watchlist, WatchlistAdmin)
