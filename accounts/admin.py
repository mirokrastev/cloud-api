from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts import models


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets


admin.site.register(models.BasicUser, CustomUserAdmin)
admin.site.register(models.StandardUser, CustomUserAdmin)
admin.site.register(models.PremiumUser, CustomUserAdmin)
admin.site.register(models.EnterpriseUser, CustomUserAdmin)
