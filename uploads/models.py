import sys

from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from base.models import BaseModel
from accounts.models import User


def get_upload_path(instance, filename):
    file = filename.split('.')
    file_ext = file.pop()

    user = instance.user

    return f'{user.username}-{user.id}/{".".join(file)}-{instance.id}.{file_ext}'


class FileUpload(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to=get_upload_path)
    file_size = models.PositiveIntegerField(blank=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        self.clean()
        self.file_size = self.file.size
        return super().save(*args, **kwargs)

    def clean(self):
        remaining_space = self.user.remaining_space - self.file.size
        if remaining_space < 0:
            raise ValidationError(_('You do not have enough space'))

    def __str__(self):
        return str(self.file)
