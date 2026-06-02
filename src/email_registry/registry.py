"""Registry for email functions."""

from __future__ import annotations

from typing import TYPE_CHECKING

from django.utils.module_loading import autodiscover_modules

if TYPE_CHECKING:
    from collections.abc import Callable


class EmailRegistry:
    def __init__(self):
        self._registry = {}

    def register(
        self,
        identifier: str,
        email_func: Callable,
        fixtures_func: Callable,
        description: str = "",
    ):
        self._registry.update(
            {
                identifier: {
                    "email_func": email_func,
                    "fixtures_func": fixtures_func,
                    "description": description,
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

    def get_description(self, identifier: str) -> str:
        return self._registry[identifier]["description"]


registry = EmailRegistry()


def autodiscover_emails():
    autodiscover_modules("emails", register_to=registry)


def register(identifier: str, fixtures: Callable, description: str = "", **kwargs) -> Callable:
    """
    Register email functions with a decorator.

    Pass in the identifier string, the fixtures function, and an optional
    human-readable description shown in the admin preview list.

    Example::

        @register("my_app.welcome", fixtures=welcome_fixtures, description="Sent to new users on signup")
        def welcome_email(user, **kwargs): ...

    """

    def _decorator(email_func: Callable) -> Callable:
        registry.register(identifier, email_func, fixtures, description)
        return email_func

    return _decorator
