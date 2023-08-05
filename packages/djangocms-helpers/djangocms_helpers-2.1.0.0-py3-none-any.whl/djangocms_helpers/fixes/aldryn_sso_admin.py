from aldryn_sso.admin import AldrynCloudUserAdmin
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _


class CustomAldrynSsoAdmin(AldrynCloudUserAdmin):
    """
    Why?
    - Read https://github.com/divio/aldryn-sso/issues/45
    - sometimes, when login in via Divio, aldryn-sso complains about `duplicate key value violates unique constraint "backend_auth_user_email_key"` 
    - in that case you need the aldryn-sso admin panel to connect the exising user to your custom user model
    - you're welcome!
    """

    def linked_user(self, obj):
        html_link = '<a href="{}">{}</a>'.format(
            reverse('admin:backend_auth_user_change', args=[obj.pk]),
            obj.user,
        )
        return mark_safe(html_link)


    linked_user.short_description = _('User')
