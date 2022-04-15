from accounts import models


def create_user(model=None,
                username='testuser',
                email='testemail@example.com',
                password='secretPassword123',
                type=models.User.Types.BASIC,
                **kwargs):
    if model is None:
        model = models.User
    return model.objects.create_user(username=username, email=email, password=password, type=type, **kwargs)
