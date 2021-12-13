import os
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from cloud.settings import MEDIA_ROOT
from uploads.models import FileUpload


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
