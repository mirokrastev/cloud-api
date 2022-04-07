import os

from cloud import settings


def delete_user_folder(instance, **kwargs):
    folder = f'{settings.MEDIA_ROOT}/{instance.username}-{instance.uuid}'
    if os.path.exists(folder):
        os.rmdir(folder)
