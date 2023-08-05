from cms.models import Title, Page
from django.dispatch import receiver
from django.db.models.signals import post_save
from fieldsignals import post_save_changed


@receiver(post_save, sender=Page)
def fix_page_slugs(sender, instance: Page, **kwargs):
    _update_child_pages(instance)


@receiver(post_save_changed, sender=Title, fields=['slug', 'path'])
def fix_title_path(sender, instance: Title, **kwargs):
    _update_child_pages(instance.page)


def _update_child_pages(page: Page):
    for language in page.get_languages():
        _update_title_path(page, language)
        for child_page in page.get_child_pages():
            _update_title_path(child_page, language)


def _update_title_path(page: Page, language: str):
    if hasattr(page.get_title_obj(language, fallback=False), 'get_path_for_base'):
        # noinspection PyProtectedMember
        page._update_title_path(language)
