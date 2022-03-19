from django.http import FileResponse

from rest_framework import viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, DestroyModelMixin
from rest_framework import parsers

from uploads.models import FileUpload
from uploads.serializers import FileUploadSerializer


class FileUploadViewSet(ListModelMixin,
                        RetrieveModelMixin,
                        CreateModelMixin,
                        DestroyModelMixin,
                        viewsets.GenericViewSet):
    serializer_class = FileUploadSerializer
    queryset = FileUpload.objects.all()
    parser_classes = [parsers.JSONParser, parsers.MultiPartParser]

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
