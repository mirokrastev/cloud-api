from django.apps import apps


def delete_user_folder(instance, **kwargs):
    # todo implement
    pass


def create_user_account(instance, created: bool, **kwargs):
    if not created:
        return

    # Get UserMore Model dynamically
    account_model = apps.get_model('accounts', '%sUserMore' % instance.type.title())
    account_model.objects.create(user=instance)
