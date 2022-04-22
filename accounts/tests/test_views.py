from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token

from accounts import models
from accounts.tests.factories import create_user


class RegisterApiTestCase(APITestCase):
    """
    Tests /register/ endpoint
    """
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('accounts:register-list')
        self.base_data = {
            'username': 'testapiuser',
            'email': 'registeruseremail@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'Password123Test',
        }

    def test_register_successful(self):
        response = self.client.post(self.url, self.base_data)
        assert response.status_code == 201

        data = response.data
        keys = ('user_id', 'token')

        assert len(data) == len(keys)
        assert (set(data.keys()) - set(keys)) == set()

        assert models.User.objects.count() == 1
        created_user = models.User.objects.get()
        assert created_user.id == data['user_id']
        assert created_user.type == models.User.Types.BASIC

        assert Token.objects.count() == 1
        created_token = Token.objects.get()
        assert created_token.key == data['token']

    def test_register_username_errors(self):
        # Create one User
        response = self.client.post(self.url, self.base_data)
        assert response.status_code == 201

        # Change email but not username
        self.base_data['email'] = 'secondtestemail@example.com'

        response = self.client.post(self.url, self.base_data)
        assert response.status_code == 400
        assert str(response.data['username'][0]) == 'A user with that username already exists.'

        self.base_data['username'] = ''
        response = self.client.post(self.url, self.base_data)
        assert response.status_code == 400
        assert str(response.data['username'][0]) == 'This field may not be blank.'

    def test_register_email_errors(self):
        # Create one User
        response = self.client.post(self.url, self.base_data)
        assert response.status_code == 201

        # Change username but not email
        self.base_data['username'] = 'testapiuser2'

        response = self.client.post(self.url, self.base_data)
        assert response.status_code == 400
        assert str(response.data['email'][0]) == 'user with this email already exists.'

        self.base_data['email'] = ''
        response = self.client.post(self.url, self.base_data)
        assert response.status_code == 400
        assert str(response.data['email'][0]) == 'This field may not be blank.'

        self.base_data['email'] = 'shouldfail'
        response = self.client.post(self.url, self.base_data)
        assert response.status_code == 400
        assert str(response.data['email'][0]) == 'Enter a valid email address.'

    def test_register_password_errors(self):
        # Create one User
        response = self.client.post(self.url, self.base_data)
        assert response.status_code == 201

        self.base_data['username'] = 'testapiuser2'
        self.base_data['email'] = 'secondtestemail@example.com'

        self.base_data['password'] = ''
        response = self.client.post(self.url, self.base_data)
        assert response.status_code == 400
        assert str(response.data['password'][0]) == 'This field may not be blank.'

        self.base_data['password'] = 'q'
        response = self.client.post(self.url, self.base_data)
        assert response.status_code == 400

        errors = ('This password is too short. It must contain at least 8 characters.',
                  'This password is too common.')
        assert len(response.data['password']) == 2
        assert all([error in errors for error in response.data['password']])


class LoginApiTestCase(APITestCase):
    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.url = reverse('accounts:login')

    def test_login_incorrect_credentials(self):
        data = {
            'username': 'testuser',
            'password': 'shouldFail123zxc'
        }

        response = self.client.post(self.url, data)
        assert response.status_code == 400

        assert response.data['non_field_errors'][0] == 'Unable to log in with provided credentials.'

        data = {
            'username': 'karkinos',
            'password': 'secretPassword123'
        }

        response = self.client.post(self.url, data)
        assert response.status_code == 400

        assert response.data['non_field_errors'][0] == 'Unable to log in with provided credentials.'

    def test_login_correct_credentials(self):
        data = {
            'username': 'testuser',
            'password': 'secretPassword123'
        }

        response = self.client.post(self.url, data)
        assert response.status_code == 200

        assert len(response.data) == 1
        assert response.data['token']


class LogoutAPiTestCase(APITestCase):
    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.url = reverse('accounts:logout')

    def test_logout_unauthorized(self):
        response = self.client.post(self.url)
        assert response.status_code == 401
        assert response.data['detail'] == 'Authentication credentials were not provided.'

    def test_logout_authorized(self):
        self.client.force_authenticate(self.user)

        response = self.client.post(self.url)
        assert response.status_code == 204


class UserApiTestcase(APITestCase):
    def setUp(self):
        self.user = create_user(models.StandardUser,
                                first_name='FName', last_name='LName',
                                type=models.User.Types.STANDARD)
        self.client = APIClient()

        self.client.force_authenticate(self.user)

    def test_unauthorized_request(self):
        self.client.logout()
        url = reverse('accounts:user-list')

        response = self.client.get(url)
        assert response.status_code == 401
        assert response.data['detail'] == 'Authentication credentials were not provided.'

    def test_user_list(self):
        url = reverse('accounts:user-list')

        response = self.client.get(url)
        assert response.status_code == 200

        data = response.data
        keys = ('id', 'username', 'first_name', 'last_name', 'email', 'type', 'space')

        assert len(data) == len(keys)
        assert (set(data.keys()) - set(keys)) == set()

        assert (data['username'], data['first_name'],
                data['last_name'], data['email'],
                data['type'], data['space']) == ('testuser', 'FName',
                                                 'LName', 'testemail@example.com',
                                                 'standard', 5 * 1024 ** 3)

    def test_user_stats(self):
        url = reverse('accounts:user-stats')

        response = self.client.get(url)
        assert response.status_code == 200

        data = response.data
        keys = ('files_count', 'used_space', 'remaining_space')

        assert len(data) == len(keys)
        assert (set(data.keys()) - set(keys)) == set()

        assert (data['files_count'],
                data['used_space'],
                data['remaining_space']) == (0, 0, 5 * 1024 ** 3)
