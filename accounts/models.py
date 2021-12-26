from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from math import inf

PROFILE_TYPES = (
    ('basic', 'Basic'),
    ('standard', 'Standard'),
    ('premium', 'Premium'),
    ('enterprise', 'Enterprise'),
)

"""
10 * 1024 ** 3 = 10 GB in bytes
50 * 1024 ** 3 = 50 GB in bytes
100 * 1024 ** 3 = 100 GB in bytes
"""


class User(AbstractUser):
    type = models.CharField(max_length=30, choices=PROFILE_TYPES, default='basic')
    email = models.EmailField(unique=True)

    @property
    def account(self):
        return getattr(self, '%susermore' % self.type)

    @property
    def remaining_space(self):
        user_uploads = self.uploads.all()
        user_uploads_size = sum(i.file.size for i in user_uploads)
        remaining_space = self.account.space - user_uploads_size
        return remaining_space


class BasicUserManager(UserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type='basic')


class BasicUserMore(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    @property
    def space(self):
        return 10 * 1024 ** 3


class BasicUser(User):
    objects = BasicUserManager()

    @property
    def account(self):
        return self.basicusermore

    class Meta:
        proxy = True


class StandardUserManager(UserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type='standard')


class StandardUserMore(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    @property
    def space(self):
        return 50 * 1024 ** 3

    def __str__(self):
        return str(self.user)


class StandardUser(User):
    objects = StandardUserManager()

    @property
    def account(self):
        return self.standardusermore

    class Meta:
        proxy = True


class PremiumUserManager(UserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type='premium')


class PremiumUserMore(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    @property
    def space(self):
        return 100 * 1024 ** 3

    def __str__(self):
        return str(self.user)


class PremiumUser(User):
    objects = PremiumUserManager()

    @property
    def account(self):
        return self.premiumusermore

    class Meta:
        proxy = True


class EnterpriseUserManager(UserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type='enterprise')


class EnterpriseUserMore(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    @property
    def space(self):
        return inf

    def __str__(self):
        return str(self.user)


class EnterpriseUser(User):
    objects = EnterpriseUserManager()

    @property
    def account(self):
        return self.enterpriseusermore

    class Meta:
        proxy = True
