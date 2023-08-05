import importlib

from django.apps import AppConfig


class DjangoCmsHelpersConfig(AppConfig):
    name = 'djangocms_helpers'

    # noinspection PyUnresolvedReferences
    def ready(self):
        is_django_cms_installed = importlib.util.find_spec('cms') is not None
        if is_django_cms_installed:
            from djangocms_helpers.monkey_patches.static_placeholder_publishing_fix import monkeypatch_cms_has_publish_permission
            from djangocms_helpers.fixes.language_slug_fix import fix_page_slugs
            from djangocms_helpers.fixes.language_slug_fix import fix_title_path
