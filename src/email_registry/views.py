"""Views for email previews."""

from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from .registry import autodiscover_emails, registry

autodiscover_emails()


@method_decorator(staff_member_required, name="dispatch")
class EmailsView(TemplateView):
    template_name = "email_registry/emails_view.html"

    def dispatch(self, request, *args, **kwargs):
        request.current_app = "email_registry"
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # Provides has_permission, site_header, site_url, etc. needed for the sidebar
        ctx.update(admin.site.each_context(self.request))
        ctx.update(self.extra_context or {})
        ctx.update(
            {
                "emails": [
                    {
                        "identifier": ident,
                        "app": ident.split(".")[0],
                        "name": ident.split(".")[1],
                        "description": registry.get_description(ident),
                    }
                    for ident in registry.get_identifiers()
                ]
            }
        )
        return ctx


@method_decorator(staff_member_required, name="dispatch")
class EmailTestView(TemplateView):
    """Render an email preview wrapped in the standard admin chrome."""

    template_name = "email_registry/email_preview.html"

    def dispatch(self, request, *args, **kwargs):
        identifier = kwargs.get("identifier")

        email_func = registry.get_email_func(identifier)
        fixtures_func = registry.get_fixtures_func(identifier)

        f_args, f_kwargs = fixtures_func(request)
        email_context = email_func(*f_args, **f_kwargs)

        app_name, email_name = registry.get_app_and_email_name(identifier)

        email_template = f"{app_name}/email/{email_name}_message.html"

        for field in ["text_template", "html_template"]:
            if value := email_context.get(field, None):
                email_template = value

        # Pre-render the email body so we can embed it in the admin wrapper
        self.rendered_email = render_to_string(
            email_template, context=email_context["context"], request=request
        )
        self.identifier = identifier
        self.email_subject = email_context.get("subject", identifier)

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(admin.site.each_context(self.request))
        ctx.update(self.extra_context or {})
        ctx.update(
            {
                "rendered_email": self.rendered_email,
                "identifier": self.identifier,
                "email_subject": self.email_subject,
            }
        )
        return ctx
