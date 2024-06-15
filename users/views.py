from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .utils import create_jwt_token
from .serializers import (
    LoginSerializer, RegisterSerializer, UserSerializer, UpdateUserSerializer,
)
from .permissions import Is_Superuser
from .models import CustomUser
import uuid
from django.core.cache import cache
from users_backend.settings import env


class Login(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = LoginSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]
        user = CustomUser.objects.filter(email=email)
        if user.exists():
            if user.first().check_password(password):
                token = create_jwt_token(user.first().id)
                return Response(
                    {"access_token": token},
                    status=status.HTTP_200_OK,
                )
        return Response(
            {"message": "Your email or password is incorrect."},
            status=status.HTTP_401_UNAUTHORIZED,
        )


class Register(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = RegisterSerializer(
            data=request.data, context={"request": request}
        )
        # First way
        # serializer.is_valid(raise_exception=True)
        # serializer.save()
        # return Response(serializer.data, status=status.HTTP_201_CREATED)

        # Second Way
        serializer.is_valid(raise_exception=True)
        is_created = serializer.get_or_create_in_one_shot(
            serializer.validated_data)
        if is_created:
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            {"message": "This user with entered email and username is exists."},
            status=status.HTTP_400_BAD_REQUEST,
        )


class UsersList(ListAPIView):
    permission_classes = (Is_Superuser,)
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()


class DeleteUser(DestroyAPIView):
    permission_classes = (Is_Superuser,)
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()


class UpdateUser(APIView):
    permission_classes = (IsAuthenticated,)

    def update_information(self, request):
        user = CustomUser.objects.get(pk=request.user.pk)
        serializer = UpdateUserSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request,  *args, **kwargs):
        return self.update_information(request=request)

    def patch(self, request,  *args, **kwargs):
        return self.update_information(request=request)


class GenerateCaptcha(APIView):
    def get(self, request):
        key_unique_id = uuid.uuid4().hex
        value_unique_id = uuid.uuid4().hex
        cache.set(
            key_unique_id, value_unique_id,
            timeout=env("EXPIRE_CAPTCHA_CODE", cast=int)
        )
        return Response(
            {"key": key_unique_id, "value": value_unique_id},
            status=status.HTTP_200_OK,
        )
