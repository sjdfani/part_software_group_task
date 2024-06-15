from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import CustomUser
from django.db.models import Q


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate(self, attrs):
        lookup = Q(email=attrs["email"]) | Q(username=attrs["username"])
        if CustomUser.objects.filter(lookup).exists():
            raise ValidationError(
                {"message": "Your email or username is exists."})
        if attrs["password1"] != attrs["password2"]:
            raise ValidationError(
                {"message": "Your entered passwords are not equal."})
        return attrs

    def create(self, validated_data):
        validated_data.pop("password1")
        password = validated_data.pop("password2")
        user = CustomUser.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        exclude = ("password",)


class UpdateUserSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    username = serializers.CharField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)

    def validate(self, attrs):
        lookup = Q(email=attrs["email"]) | Q(username=attrs["username"])
        if CustomUser.objects.filter(lookup).exists():
            raise ValidationError(
                {"message": "Your email or username is exists."})
        if attrs["password1"] != attrs["password2"]:
            raise ValidationError(
                {"message": "Your entered passwords are not equal."})
        return attrs

    def update(self, instance, validated_data):
        instance.email = validated_data.get("email", instance.email)
        instance.username = validated_data.get("username", instance.username)
        instance.first_name = validated_data.get(
            "first_name", instance.first_name)
        instance.last_name = validated_data.get(
            "last_name", instance.last_name)
        instance.save()
        return instance
