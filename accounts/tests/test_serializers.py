from django.test import TestCase

from accounts import serializers
from accounts.tests.factories import create_user


class UserSerializerTestCase(TestCase):
    def setUp(self):
        self.user = create_user(email='testemail@example.com',
                                username='testuser',
                                first_name='')

    def test_user_serializer(self):
        serializer = serializers.UserSerializer(self.user).data
        keys = ('id', 'username', 'first_name', 'last_name', 'email', 'type', 'space')

        assert len(serializer.keys()) == len(keys)

        # Test if all serializer keys match keys
        assert (set(serializer.keys()) - set(keys)) == set()

        assert (serializer['email'],
                serializer['username'],
                serializer['first_name']) == ('testemail@example.com', 'testuser', '')
