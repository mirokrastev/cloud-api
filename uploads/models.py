from django.db import models

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

    def __str__(self):
        return str(self.file)
