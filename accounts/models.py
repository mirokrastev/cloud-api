import uuid
from math import inf

from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

from accounts import signals

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
    uuid = models.CharField(unique=True, max_length=32, blank=True)

    def __init__(self, *args, **kwargs):
        """
        Used to call signals from Proxy subclass models.
        """
        super().__init__(*args, **kwargs)
        models.signals.pre_delete.connect(signals.delete_user_folder, sender=self.__class__)
        models.signals.post_save.connect(signals.create_user_account, sender=self.__class__)

    def save(self, *args, **kwargs):
        if self.pk:
            return super().save(*args, **kwargs)

        temp_uuid = uuid.uuid4().hex[:10]

        if User.objects.filter(uuid=temp_uuid).count() > 0:
            return self.save(*args, **kwargs)
        self.uuid = temp_uuid
        return super().save(*args, **kwargs)

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

    def __str__(self):
        return str(self.user)


class BasicUser(User):
    objects = BasicUserManager()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = 'basic'
        return super().save(*args, **kwargs)

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

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = 'standard'
        return super().save(*args, **kwargs)

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

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = 'premium'
        return super().save(*args, **kwargs)

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

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = 'enterprise'
        return super().save(*args, **kwargs)

    @property
    def account(self):
        return self.enterpriseusermore

    class Meta:
        proxy = True
