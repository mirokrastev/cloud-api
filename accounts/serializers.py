from math import inf

from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

from accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, trim_whitespace=False, style={'input_type': 'password'})
    type = serializers.ChoiceField(choices=User.Types.choices, read_only=True)
    space = serializers.SerializerMethodField()

    def validate_password(self, value):
        if not validate_password(value):
            return value

    def get_space(self, obj):
        if obj.account.space == inf:
            return 'inf'
        return obj.account.space

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password', 'type', 'space')
