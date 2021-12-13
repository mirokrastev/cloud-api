from rest_framework import permissions, viewsets
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin
from rest_framework import parsers
from rest_framework.response import Response
from rest_framework.views import APIView
from uploads.models import FileUpload
from uploads.serializers import FileUploadSerializer


class StatsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_uploads = FileUpload.objects.filter(user=request.user)
        user_uploads_size = sum(i.file.size for i in user_uploads) / float(1 << 20)
        remaining_space = request.user.account.space - user_uploads_size

        return Response({
            'uploads_count': user_uploads.count(),
            'used_space': round(user_uploads_size, 2),
            'remaining_space': round(remaining_space, 2),
        })


class FileUploadViewSet(CreateModelMixin, ListModelMixin, RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = FileUploadSerializer
    queryset = FileUpload.objects.all()
    parser_classes = [parsers.JSONParser, parsers.MultiPartParser]

    def perform_create(self, serializer):
        serializer.validated_data['user'] = self.request.user
        return super().perform_create(serializer)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
