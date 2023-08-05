from typing import Callable

from cms.cms_toolbars import PageToolbar
from cms.utils import page_permissions


def monkeypatch_cms_has_publish_permission() -> Callable:

    def has_publish_permission(self: PageToolbar) -> bool:
        is_has_publish_permission = False

        is_page_model_available = self.page is not None
        if is_page_model_available:
            is_has_publish_permission = page_permissions.user_can_publish_page(
                self.request.user,
                page=self.page,
                site=self.current_site,
            )

        is_need_to_check_dirty_static_placeholders_perms = (
            (is_has_publish_permission or not is_page_model_available) and self.statics
        )
        if is_need_to_check_dirty_static_placeholders_perms:
            is_has_publish_permission = all(sp.has_publish_permission(self.request) for sp in self.dirty_statics)

        return is_has_publish_permission

    return has_publish_permission


PageToolbar.has_publish_permission = monkeypatch_cms_has_publish_permission()
