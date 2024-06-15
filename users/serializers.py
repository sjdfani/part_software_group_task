from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import CustomUser
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
from .utils import check_captcha_code


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    key_unique_id = serializers.CharField()
    value_unique_id = serializers.CharField()

    def validate(self, attrs):
        result = check_captcha_code(attrs)
        if not isinstance(result, tuple):
            return attrs
        raise ValidationError(result[1])


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    key_unique_id = serializers.CharField()
    value_unique_id = serializers.CharField()

    def validate(self, attrs):
        # lookup = Q(email=attrs["email"]) | Q(username=attrs["username"])
        # if CustomUser.objects.filter(lookup).exists():
        #     raise ValidationError(
        #         {"message": "Your email or username is exists."})

        if attrs["password1"] != attrs["password2"]:
            raise ValidationError(
                {"passwords": "Your entered passwords are not equal."})
        result = check_captcha_code(attrs)
        if not isinstance(result, tuple):
            return attrs
        raise ValidationError(result[1])

    def create(self, validated_data):
        validated_data.pop("password1")
        password = validated_data.pop("password2")
        user = CustomUser.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def get_or_create_in_one_shot(self, validated_data):
        try:
            user, is_created = CustomUser.objects.get_or_create(
                email=validated_data["email"],
                username=validated_data["username"],
                first_name=validated_data["first_name"],
                last_name=validated_data["last_name"],
                password=make_password(validated_data["password2"]),
            )
            return is_created
        except IntegrityError as e:
            print(e)
            if 'unique constraint' in str(e).lower() and 'email' in str(e).lower():
                raise ValidationError(
                    {"message": "This email is already registered."})
            elif 'unique constraint' in str(e).lower() and 'username' in str(e).lower():
                raise ValidationError(
                    {"message": "This username is already taken."})
            else:
                raise ValidationError(
                    {"message": "A database integrity error occurred. Please try again."})
        except Exception as e:
            raise ValidationError(
                {"message": "An unexpected error occurred. Please try again."})


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
