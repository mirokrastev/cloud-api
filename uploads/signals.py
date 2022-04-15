import os
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from uploads.models import FileUpload


@receiver(pre_delete, sender=FileUpload)
def delete_upload_file(instance, **kwargs):
    file = instance.file.path
    if os.path.exists(file):
        os.remove(file)
