from rest_framework import serializers
from .models import CustomUser


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate_email(self, value):
        if not CustomUser.objects.filter(email=value):
            raise serializers.ValidationError("This email is not exists.")
        return value
