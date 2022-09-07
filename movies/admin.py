from django.contrib import admin

from movies.models import ServiceMovie, Movie, Notification, Watchlist
from utils import export_as_csv_action


class ServiceMovie_Inline(admin.StackedInline):
    model = ServiceMovie
    extra = 1


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    inlines = (ServiceMovie_Inline,)
    actions = [
        export_as_csv_action(
            "Export selection to CSV file",
            fields=list_display,
            header=True,
            force_fields=True,
        ),
    ]


class Notification_Inline(admin.StackedInline):
    model = Notification
    extra = 2


@admin.register(Watchlist)
class WatchlistAdmin(admin.ModelAdmin):
    def watchlist_movie_name(self, obj: Watchlist) -> str:
        """
        Return the movie name.
        """
        return obj.movie.name

    def watchlist_user_name(self, obj: Watchlist) -> str:
        """
        Return the user name.
        """
        return obj.user.username

    def notifications(self, obj: Watchlist) -> str:
        """
        Return a display list of notifications.
        """
        notifications = []
        for item in obj.notification_set.all():
            notifications.append(
                f"{item.get_type_display()}/{'Y' if item.notified else 'N'}"
            )
        return " ".join(notifications)

    list_display = ("watchlist_movie_name", "watchlist_user_name", "notifications")
    search_fields = ("movie__name", "user__name", "user__email")
    inlines = (Notification_Inline,)
    actions = [
        export_as_csv_action(
            "Export selection to CSV file",
            fields=list_display,
            header=True,
            force_fields=True,
        ),
    ]
