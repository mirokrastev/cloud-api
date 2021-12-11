from django.contrib import admin

# Register your models here.
from uploads.models import FileUpload

admin.site.register(FileUpload)