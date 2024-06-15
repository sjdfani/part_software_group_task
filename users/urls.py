from django.urls import path
from .views import (
    Login, Register, UsersList,
)

app_name = "users"

urlpatterns = [
    path("login/", Login.as_view(), name="Login"),
    path("register/", Register.as_view(), name="Register"),
    path("list/", UsersList.as_view(), name="UsersList"),
]
