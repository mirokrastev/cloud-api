import os
from django.apps import apps

from cloud import settings


def delete_user_folder(instance, **kwargs):
    p = f'{settings.MEDIA_ROOT}/{instance.username}-{instance.uuid}'
    if os.path.exists(p):
        os.rmdir(p)


def create_user_account(instance, created: bool, **kwargs):
    if not created:
        return

    # Get UserMore Model dynamically
    account_model = apps.get_model('accounts', '%sUserMore' % instance.type.title())
    account_model.objects.create(user=instance)
