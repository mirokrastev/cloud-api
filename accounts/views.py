from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.viewsets import mixins
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from accounts import models
from accounts import serializers


class LoginView(ObtainAuthToken):
    pass


class RegisterViewSet(mixins.CreateModelMixin, GenericViewSet):
    queryset = models.BasicUser.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = ()


class UserDetail(APIView):
    serializer_class = serializers.UserSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        self.request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
