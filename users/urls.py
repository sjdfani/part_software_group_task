from django.urls import path
from .views import (
    Login, Register, UsersList, DeleteUser, UpdateUser, GenerateCaptcha,
)

app_name = "users"

urlpatterns = [
    path("captcha/generate/", GenerateCaptcha.as_view(), name="GenerateCaptcha"),

    path("login/", Login.as_view(), name="Login"),
    path("register/", Register.as_view(), name="Register"),
    path("list/", UsersList.as_view(), name="UsersList"),
    path("<int:pk>/delete/", DeleteUser.as_view(), name="DeleteUser"),
    path("update/", UpdateUser.as_view(), name="UpdateUser"),
]
