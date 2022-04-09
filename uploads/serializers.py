from rest_framework import serializers
from uploads import models


class FileUploadSerializer(serializers.ModelSerializer):
    file = serializers.FileField(max_length=100, write_only=True, required=True, allow_null=False)

    file_name = serializers.SerializerMethodField(read_only=True)
    file_size = serializers.IntegerField(read_only=True)

    def get_file_name(self, obj):
        _, file_name = obj.file.file.name.split(f'{obj.user.username}-{obj.user.id}', maxsplit=1)
        return file_name[1:]

    class Meta:
        model = models.FileUpload
        fields = ['id', 'file', 'file_name', 'file_size', 'created_at']
