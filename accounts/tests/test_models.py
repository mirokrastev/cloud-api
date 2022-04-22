from math import inf

from django.test import TestCase

from accounts import models
from accounts.tests.factories import create_user


class UserModelTestCase(TestCase):
    def test_create_user(self):
        user = create_user(email='testemail1@example.com')

        assert user
        assert user.username == 'testuser'
        assert user.email == 'testemail1@example.com'
        assert user.type == 'basic'
        assert isinstance(user.account, models.BasicUser)


class BasicUserTestCase(TestCase):
    def setUp(self):
        self.user = create_user(username='basicuser')

    def test_user_proxy_model(self):
        assert isinstance(self.user, models.User)
        assert not isinstance(self.user, models.BasicUser)

        assert isinstance(self.user.account, models.BasicUser)
        assert self.user.account == self.user

    def test_user_space(self):
        assert self.user.account.space == 1073741824  # 1 GB in bytes

    def test_proxy_model_user_creation(self):
        proxy_user = models.BasicUser.objects.create_user(username='basicuser2',
                                                          email='testemail2@example.com',
                                                          password='secretPassword123',
                                                          type=models.User.Types.BASIC)

        assert proxy_user
        assert proxy_user.username == 'basicuser2'
        assert isinstance(proxy_user, models.User)


class StandardUserTestCase(TestCase):
    def setUp(self):
        self.user = create_user(username='standarduser', type=models.User.Types.STANDARD)

    def test_user_proxy_model(self):
        assert isinstance(self.user, models.User)
        assert not isinstance(self.user, models.StandardUser)

        assert isinstance(self.user.account, models.StandardUser)
        assert self.user.account == self.user

    def test_user_space(self):
        assert self.user.account.space == 5368709120  # 5 GB in bytes

    def test_proxy_model_user_creation(self):
        proxy_user = create_user(models.StandardUser,
                                 username='standarduser2',
                                 email='testemail2@example.com',
                                 type=models.User.Types.STANDARD)

        assert proxy_user
        assert proxy_user.username == 'standarduser2'
        assert isinstance(proxy_user, models.User)


class PremiumUserTestCase(TestCase):
    def setUp(self):
        self.user = create_user(username='premiumser',
                                type=models.User.Types.PREMIUM)

    def test_user_proxy_model(self):
        assert isinstance(self.user, models.User)
        assert not isinstance(self.user, models.PremiumUser)

        assert isinstance(self.user.account, models.PremiumUser)
        assert self.user.account == self.user

    def test_user_space(self):
        assert self.user.account.space == 10737418240  # 10 GB in bytes

    def test_proxy_model_user_creation(self):
        proxy_user = create_user(models.PremiumUser,
                                 username='premiumuser2',
                                 email='testemail2@example.com',
                                 type=models.User.Types.PREMIUM)

        assert proxy_user
        assert proxy_user.username == 'premiumuser2'
        assert isinstance(proxy_user, models.User)


class EnterpriseUserTestCase(TestCase):
    def setUp(self):
        self.user = create_user(username='enterpriseuser',
                                type=models.User.Types.ENTERPRISE)

    def test_user_proxy_model(self):
        assert isinstance(self.user, models.User)
        assert not isinstance(self.user, models.EnterpriseUser)

        assert isinstance(self.user.account, models.EnterpriseUser)
        assert self.user.account == self.user

    def test_user_space(self):
        assert self.user.account.space == inf

    def test_proxy_model_user_creation(self):
        proxy_user = create_user(models.EnterpriseUser,
                                 username='enterpriseuser2',
                                 email='testemail2@example.com',
                                 type=models.User.Types.ENTERPRISE)

        assert proxy_user
        assert proxy_user.username == 'enterpriseuser2'
        assert isinstance(proxy_user, models.User)
