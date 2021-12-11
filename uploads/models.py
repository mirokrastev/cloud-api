from django.db import models
import uuid
from accounts.models import User


def get_upload_path(instance, filename):
    file = filename.split('.')
    file_ext = file.pop()
    return f'{instance.user.username}/{".".join(file)}-{uuid.uuid4().hex[:10]}.{file_ext}'


class FileUpload(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploads')
    file = models.FileField(upload_to=get_upload_path)
