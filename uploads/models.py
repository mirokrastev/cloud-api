from django.db import models
import uuid

# Create your models here.
from accounts.models import User


def get_upload_path(instance, filename):
    file, file_ext = filename.split('.')
    return f'{instance.user.username}/{file}-{uuid.uuid4().hex[:10]}.{file_ext}'


class FileUpload(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploads')
    file = models.FileField(upload_to=get_upload_path)
