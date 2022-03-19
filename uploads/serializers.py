from rest_framework import serializers
from uploads import models


class FileUploadSerializer(serializers.ModelSerializer):
    filename = serializers.SerializerMethodField(read_only=True)
    file = serializers.FileField(max_length=100, write_only=True, required=True, allow_null=False)

    def get_filename(self, obj):
        _, filename = obj.file.file.name.split(f'{obj.user.username}-{obj.user.id}', maxsplit=1)
        return filename[1:]

    class Meta:
        model = models.FileUpload
        fields = ['id', 'file', 'filename']
