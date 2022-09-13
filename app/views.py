from django.conf import settings
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view

from movies.models import SERVICE_CHOICES, NOTIFICATION_CHOICES
from rest_framework.views import APIView
from django.views.generic.base import TemplateView

from .version import VERSION


class ConfigurationView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request: Request) -> Response:
        """
        Expose the configuration settings to the UI clients.
        """
        data = dict(
            google_key=settings.SOCIAL_AUTH_GOOGLE_PLUS_KEY,
            service_choices=SERVICE_CHOICES,
            notification_choices=NOTIFICATION_CHOICES,
        )

        return Response(data)


class HomepageView(TemplateView):
    template_name = "app/coming_soon.html"


@api_view(["GET"])
def version(request: Request) -> Response:
    """
    Return the application version.
    """
    return Response({"version": VERSION})
