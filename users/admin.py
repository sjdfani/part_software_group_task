from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserChangeForm, CustomUserCreationForm


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    readonly_fields = ("date_joined", "last_login")
    list_display = (
        "email", "username", "is_active", "is_staff", "is_superuser")
    list_filter = ("is_staff", "is_active", "is_superuser")
    fieldsets = (
        ('Personal Information', {
         "fields": ("email", "username", "first_name", "last_name", "password")}),
        ("Permissions", {"fields": (
            "is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Date and Time", {
         "fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        ('Personal Information', {
            "classes": ("wide",),
            "fields": ("email", "username", "first_name", "last_name", "password1", "password2")}),
        ("Permissions", {"fields": (
            "is_active", "is_staff",  "is_superuser", "groups", "user_permissions")}),
    )
    search_fields = ("email",)
    ordering = ("email",)
    readonly_fields = ("date_joined", "last_login")


admin.site.register(CustomUser, CustomUserAdmin)
