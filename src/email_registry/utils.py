"""Utility for sending email."""

import regex as re
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from .registry import registry


def textify(html_text):
    """
    Produce a reasonable text version of HTML.
    """
    # Remove html tags and continuous whitespaces
    text_only = re.sub("[ \t]+", " ", strip_tags(html_text))
    # Strip single spaces in the beginning of each line
    return text_only.replace("\n ", "\n").strip()


def send_mail(
    identifier: str,
    *email_args,
    recipients: list[str] | None = None,
    cc_recipients: list[str] | None = None,
    bcc_recipients: list[str] | None = None,
    from_email: str | None = None,
    **email_kwargs,
):
    email_kwargs = {"from_email": from_email, "recipients": recipients} | email_kwargs

    email_func = registry.get_email_func(identifier)
    email_kwargs = email_func(*email_args, **email_kwargs)

    app_name, email_name = registry.get_app_and_email_name(identifier)

    if (from_email := email_kwargs.get("from_email", None)) is None:
        from_email = settings.FROM_EMAIL

    if (recipients := email_kwargs.get("recipients", None)) is None:
        recipients = [x[1] for x in settings.MANAGERS]

    if getattr(settings, "EMAIL_DEBUG", False):
        recipients = [settings.ADMINS[0][1]]

    context = email_kwargs.get("context")
    subject = email_kwargs.get("subject")
    if not subject:
        subject_template = email_kwargs.get(
            "subject_template", f"{app_name}/email/{email_name}_subject.txt"
        )
        subject = render_to_string(subject_template, context=context)

    html_message = None
    plain_text = None
    alternatives = None

    # Attachments are expected to be a list of tuples
    # The tuple is (filename, content, content type)
    attachments = email_kwargs.get("attachments")

    html_template = email_kwargs.get(
        "html_template", f"{app_name}/email/{email_name}_message.html"
    )
    if html_template:
        html_message = render_to_string(html_template, context=context)
        alternatives = [(html_message, "text/html")]

    text_template = email_kwargs.get("text_template", f"{app_name}/email/{email_name}.txt")
    if text_template:
        plain_text = render_to_string(text_template, context=context)

    if html_message and not plain_text:
        plain_text = textify(html_message)

    email = EmailMultiAlternatives(
        subject=subject,
        body=plain_text,
        from_email=from_email,
        reply_to=[settings.DEFAULT_NOREPLY_EMAIL],
        to=recipients,
        cc=cc_recipients,
        bcc=bcc_recipients,
        alternatives=alternatives,
        attachments=attachments,
    )
    email.send(fail_silently=False)
