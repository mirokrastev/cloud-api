from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext as _

from accounts import models


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (_('Additional info'), {'fields': ('type',)}),
    )


admin.site.register(models.BasicUser, CustomUserAdmin)
admin.site.register(models.BasicUserMore)

admin.site.register(models.StandardUser, CustomUserAdmin)
admin.site.register(models.StandardUserMore)

admin.site.register(models.PremiumUser, CustomUserAdmin)
admin.site.register(models.PremiumUserMore)

admin.site.register(models.EnterpriseUser, CustomUserAdmin)
admin.site.register(models.EnterpriseUserMore)
