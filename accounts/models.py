from math import inf

from django.db import models
from django.apps import apps
from django.contrib.auth.models import AbstractUser, UserManager
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.utils.functional import cached_property

from accounts import signals
from base.models import BaseModel


class User(BaseModel, AbstractUser):
    class Types(models.TextChoices):
        BASIC = ('basic', 'Basic')
        STANDARD = ('standard', 'Standard')
        PREMIUM = ('premium', 'Premium')
        ENTERPRISE = ('enterprise', 'Enterprise')

    type = models.CharField(max_length=30, choices=Types.choices, default=Types.BASIC)
    email = models.EmailField(unique=True)

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'type']

    class Meta:
        ordering = ['-created_at']

    def __init__(self, *args, **kwargs):
        """
        Used to call signals from Proxy subclass models.
        """
        super().__init__(*args, **kwargs)
        models.signals.pre_delete.connect(signals.delete_user_folder, sender=self.__class__)

    @cached_property
    def account(self):
        proxy_model = apps.get_model('accounts', '%sUser' % self.type.capitalize())
        return proxy_model.objects.get(id=self.id)

    @cached_property
    def used_space(self):
        return self.files.all().aggregate(size=Coalesce(Sum('file_size'), 0))['size']

    @cached_property
    def remaining_space(self):
        remaining_space = self.account.space - self.used_space
        return remaining_space


class BasicUserManager(UserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type='basic')


class BasicUser(User):
    objects = BasicUserManager()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = User.Types.BASIC
        return super().save(*args, **kwargs)

    @property
    def space(self):
        return 10 * 1024 ** 3  # 10 GB in bytes

    class Meta:
        proxy = True


class StandardUserManager(UserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type='standard')


class StandardUser(User):
    objects = StandardUserManager()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = User.Types.STANDARD
        return super().save(*args, **kwargs)

    @property
    def space(self):
        return 50 * 1024 ** 3  # 50 GB in bytes

    class Meta:
        proxy = True


class PremiumUserManager(UserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type='premium')


class PremiumUser(User):
    objects = PremiumUserManager()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = User.Types.PREMIUM
        return super().save(*args, **kwargs)

    @property
    def space(self):
        return 100 * 1024 ** 3  # 100 GB in bytes

    class Meta:
        proxy = True


class EnterpriseUserManager(UserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type='enterprise')


class EnterpriseUser(User):
    objects = EnterpriseUserManager()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = User.Types.ENTERPRISE
        return super().save(*args, **kwargs)

    @property
    def space(self):
        return inf

    class Meta:
        proxy = True
