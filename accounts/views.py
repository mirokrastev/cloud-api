from math import inf

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
    queryset = models.BasicUser.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = ()


class UserViewSet(ViewSet):
    serializer_class = serializers.UserSerializer

    def list(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data)

    @action(methods=['GET'], detail=False)
    def stats(self, request, *args, **kwargs):
        user_uploads = self.request.user.uploads.all()

        used_space = round(sum(i.file.size for i in user_uploads), 2)
        remaining_space = round(self.request.user.account.space - used_space, 2)
        remaining_space = 'inf' if remaining_space == inf else remaining_space

        return Response({
            'uploads_count': user_uploads.count(),
            'used_space': used_space,
            'remaining_space': remaining_space,
        })


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        self.request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
