import sys
from math import inf

from django.http import FileResponse

from rest_framework import permissions, viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, DestroyModelMixin
from rest_framework import parsers
from rest_framework.response import Response
from rest_framework.views import APIView

from uploads.models import FileUpload
from uploads.serializers import FileUploadSerializer


class StatsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_uploads = self.request.user.uploads.all()

        used_space = round(sum(i.file.size for i in user_uploads), 2)
        remaining_space = round(self.request.user.account.space - used_space, 2)
        remaining_space = 'inf' if remaining_space == inf else remaining_space

        return Response({
            'uploads_count': user_uploads.count(),
            'used_space': used_space,
            'remaining_space': remaining_space,
        })


class FileUploadViewSet(DestroyModelMixin, CreateModelMixin, ListModelMixin, RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = FileUploadSerializer
    queryset = FileUpload.objects.all()
    parser_classes = [parsers.JSONParser, parsers.MultiPartParser]

    def perform_create(self, serializer):
        # todo: return error

        remaining_space = self.request.user.remaining_space - sys.getsizeof(serializer.validated_data['file'].file)
        if remaining_space >= 0:
            serializer.save(user=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class FileDownloadView(GenericAPIView):
    queryset = FileUpload.objects.all()
    serializer_class = None

    def get(self, request, *args, **kwargs):
        file = self.get_object()
        return FileResponse(open(file.file.path, mode='rb'), as_attachment=True)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
