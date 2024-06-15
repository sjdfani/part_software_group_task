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
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


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
