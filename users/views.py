from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from .utils import create_jwt_token
from .serializers import (
    LoginSerializer, RegisterSerializer,
)


class Login(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = LoginSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]
        user = authenticate(email=email, password=password)
        if user is not None:
            token = create_jwt_token(user.id)
            return Response(
                {"access_token": token},
                status=status.HTTP_200_OK,
            )
        else:
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
