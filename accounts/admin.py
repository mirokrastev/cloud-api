from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.models import BasicUser, BasicUserMore

admin.site.register(BasicUser, UserAdmin)
admin.site.register(BasicUserMore)
