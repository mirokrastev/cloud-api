from math import inf

from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ViewSet
from rest_framework.viewsets import mixins
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from accounts import models
from accounts import serializers


class LoginView(ObtainAuthToken):
    pass


class RegisterViewSet(mixins.CreateModelMixin, GenericViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = ()

    def perform_create(self, serializer):
        return serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = self.perform_create(serializer)
        token, created = Token.objects.get_or_create(user=user)
        return Response({'user_id': user.id, 'token': token.key}, status=status.HTTP_201_CREATED)


class UserViewSet(ViewSet):
    serializer_class = serializers.UserSerializer

    def list(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data)

    @action(methods=['GET'], detail=False)
    def stats(self, request, *args, **kwargs):
        user = self.request.user

        used_space = round(user.used_space, 2)
        remaining_space = round(user.remaining_space, 2)
        remaining_space = 'inf' if remaining_space == inf else remaining_space

        return Response({
            'files_count': user.files.count(),
            'used_space': used_space,
            'remaining_space': remaining_space,
        })


class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        self.request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
