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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploads')
    file = models.FileField(upload_to=get_upload_path)
    date = models.DateTimeField(auto_now_add=True)

    def clean(self):
        remaining_space = self.user.remaining_space - sys.getsizeof(self.file.file)
        if remaining_space < 0:
            raise ValidationError(_('You do not have enough space'))

    def __str__(self):
        return str(self.file)
