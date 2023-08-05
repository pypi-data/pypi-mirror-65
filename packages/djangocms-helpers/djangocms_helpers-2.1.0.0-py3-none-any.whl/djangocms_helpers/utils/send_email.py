from typing import Dict

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django_settings_export import settings_export


def send_email(
    email_subject: str,
    template_path_without_extension: str,
    template_context: dict = None,
    email_destination: str = None,
    email_headers: Dict[str, str] = None,
    email_from: str = settings.DEFAULT_FROM_EMAIL,
    email_reply_to: str = None,
):
    template_plaintext = get_template(f'{template_path_without_extension}.txt')
    template_context = _get_full_context(context_base=template_context)
    if email_reply_to:
        reply_to_header = {'Reply-To': email_reply_to}
        if email_headers is None:
            email_headers = reply_to_header
        else:
            email_headers = {**email_headers, **reply_to_header}
    email = EmailMultiAlternatives(
        subject=email_subject,
        body=template_plaintext.render(template_context),
        from_email=email_from,
        to=[email_destination],
        headers=email_headers,
    )
    template_html = get_template(f'{template_path_without_extension}.html')
    email.attach_alternative(template_html.render(template_context), 'text/html')
    email.send()


def _get_full_context(context_base: dict = None) -> dict:
    settings_exported = settings_export(request=None)
    settings_exported['site'] = Site.objects.get_current()
    settings_exported['base_url'] = settings.META_SITE_PROTOCOL + '://' + Site.objects.get_current().domain
    if context_base is None:
        return settings_exported
    else:
        return {**context_base, **settings_exported}
