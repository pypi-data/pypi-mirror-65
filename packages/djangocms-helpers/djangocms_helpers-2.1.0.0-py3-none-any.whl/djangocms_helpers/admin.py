from aldryn_sso.models import AldrynCloudUser
from django.contrib import admin
from djangocms_helpers.fixes.aldryn_sso_admin import CustomAldrynSsoAdmin


admin.site.unregister(AldrynCloudUser)  # https://github.com/divio/aldryn-sso/issues/45
admin.site.register(AldrynCloudUser, CustomAldrynSsoAdmin)
