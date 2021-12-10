from math import inf

from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

from accounts.models import User, PROFILE_TYPES


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, trim_whitespace=False, style={'input_type': 'password'})
    type = serializers.ChoiceField(choices=PROFILE_TYPES, read_only=True)
    space = serializers.SerializerMethodField()

    def validate_password(self, value):
        if not validate_password(value):
            return value

    def get_space(self, obj):
        if obj.account.space == inf:
            return 'inf'

        space_in_gb = obj.account.space / 1000
        return space_in_gb

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)

        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password', 'type', 'space')
