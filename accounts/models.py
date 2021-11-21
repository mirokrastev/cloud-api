from django.db import models
from django.contrib.auth.models import AbstractUser

PROFILE_TYPES = (
    ('basic', 'Basic'),
    ('standard', 'Standard'),
    ('premium', 'Premium'),
    ('enterprise', 'Enterprise'),
)


class User(AbstractUser):
    type = models.CharField(max_length=30, choices=PROFILE_TYPES, default='basic')
    email = models.EmailField(unique=True)


class BasicUserManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type='basic')


class BasicUserMore(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class BasicUser(User):
    objects = BasicUserManager()

    @property
    def more(self):
        return self.basicusermore

    class Meta:
        proxy = True


class StandardUserManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type='standard')


class StandardUserMore(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class StandardUser(User):
    objects = StandardUserManager()

    @property
    def more(self):
        return self.standardusermore

    class Meta:
        proxy = True


class PremiumUserManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type='premium')


class PremiumUserMore(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class PremiumUser(User):
    objects = PremiumUserManager()

    @property
    def more(self):
        return self.premiumusermore

    class Meta:
        proxy = True


class EnterpriseUserManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type='enterprise')


class EnterpriseUserMore(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class EnterpriseUser(User):
    objects = PremiumUserManager()

    @property
    def more(self):
        return self.enterpriseusermore

    class Meta:
        proxy = True
