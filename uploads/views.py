from django.http import FileResponse

from rest_framework import viewsets
from rest_framework.decorators import action
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

    @action(detail=True, url_name='download')
    def download(self, request, *args, **kwargs):
        file = self.get_object()
        return FileResponse(open(file.file.path, mode='rb'), as_attachment=True)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
