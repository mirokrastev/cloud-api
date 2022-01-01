from django.db import models
import uuid
from accounts.models import User


def get_upload_path(instance, filename):
    file = filename.split('.')
    file_ext = file.pop()

    user = instance.user
    temp_uuid = uuid.uuid4().hex[:10]

    return f'{user.username}-{user.uuid}/{".".join(file)}-{temp_uuid}.{file_ext}'


class FileUpload(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploads')
    file = models.FileField(upload_to=get_upload_path)
    date = models.DateTimeField(auto_now_add=True)
    # todo add uuid to model

    def __str__(self):
        return str(self.file)
