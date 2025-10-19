"""
Email sending functions.
"""

from django.conf import settings

from email_registry.registry import register


def hello_fixtures(request) -> tuple[list, dict]:
    """
    Provide a sample for display.
    """
    return ["Hello world"], {}


@register("hello_world.hello", hello_fixtures)
def hello(
    message,
    **kwargs,
) -> dict:
    recipient_list = [email for _, email in settings.ADMINS]
    return {
        **kwargs,
        "subject": "Hello World",
        "recipients": recipient_list,
        "html_template": "hello_world/admin/email/hello.html",
        "text_template": None,
        "context": {
            "title": "Hello World",
            "message": message,
        },
    }
