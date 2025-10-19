"""Views for email previews."""

from django.contrib.admin.views.decorators import staff_member_required
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
        ctx.update({"emails": registry.get_identifiers()})
        return ctx


@method_decorator(staff_member_required, name="dispatch")
class EmailTestView(TemplateView):
    def dispatch(self, request, *args, **kwargs):
        identifier = kwargs.get("identifier")

        email_func = registry.get_email_func(identifier)
        fixtures_func = registry.get_fixtures_func(identifier)

        f_args, f_kwargs = fixtures_func(request)
        self.email_context = email_func(*f_args, **f_kwargs)

        app_name, email_name = registry.get_app_and_email_name(identifier)

        self.template_name = f"{app_name}/email/{email_name}_message.html"
        for template_field in ["text_template", "html_template"]:
            if template_name := self.email_context.get(template_field, None):
                self.template_name = template_name

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(self.email_context["context"])
        return ctx
