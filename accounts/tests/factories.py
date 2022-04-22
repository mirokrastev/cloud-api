from rest_framework.authtoken.models import Token

from accounts import models


def create_user(model=None,
                username='testuser',
                email='testemail@example.com',
                password='secretPassword123',
                type=models.User.Types.BASIC,
                create_token=True,
                **kwargs):
    if model is None:
        model = models.User

    user = model.objects.create_user(username=username, email=email, password=password, type=type, **kwargs)

    if create_token:
        Token.objects.get_or_create(user=user)

    return user
