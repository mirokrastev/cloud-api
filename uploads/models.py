from django.db import models
import uuid
from accounts.models import User


def get_upload_path(instance, filename):
    file = filename.split('.')
    file_ext = file.pop()

    user = instance.user

    return f'{user.username}-{user.uuid}/{".".join(file)}-{instance.uuid}.{file_ext}'


class FileUpload(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploads')
    file = models.FileField(upload_to=get_upload_path)
    date = models.DateTimeField(auto_now_add=True)
    uuid = models.CharField(unique=True, max_length=32, blank=True)

    def __str__(self):
        return str(self.file)

    def save(self, *args, **kwargs):
        if self.pk:
            return super().save(*args, **kwargs)

        temp_uuid = uuid.uuid4().hex[:10]

        if FileUpload.objects.filter(uuid=temp_uuid).count() > 0:
            return self.save(*args, **kwargs)
        self.uuid = temp_uuid
        return super().save(*args, **kwargs)
