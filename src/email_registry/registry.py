"""Registry for email functions."""

from collections.abc import Callable

from django.utils.module_loading import autodiscover_modules


class EmailRegistry:
    def __init__(self):
        self._registry = {}

    def register(self, identifier, email_func, fixtures_func):
        self._registry.update(
            {
                identifier: {
                    "email_func": email_func,
                    "fixtures_func": fixtures_func,
                }
            }
        )

    def get_app_and_email_name(self, identifier):
        split = identifier.split(".")
        return split[0], split[1]

    def get_identifiers(self):
        return sorted(self._registry.keys())

    def get_email_func(self, identifier: str):
        return self._registry[identifier]["email_func"]

    def get_fixtures_func(self, identifier: str):
        return self._registry[identifier]["fixtures_func"]


registry = EmailRegistry()


def autodiscover_emails():
    autodiscover_modules("emails", register_to=registry)


def register(identifier: str, fixtures: Callable, **kwargs):
    """
    Register email functions with a decorator.

    Pass in the identifer string and the fixtures function.

    """

    def _decorator(email_func):
        registry.register(identifier, email_func, fixtures)
        return email_func

    return _decorator
