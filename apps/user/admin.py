from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.user import forms as user_forms
from apps.user import models as user_models


@admin.register(user_models.User)
class CustomUserAdmin(UserAdmin):
    """
    Custom admin configuration for User model.

    Handles user creation, updates, permissions,
    and admin interface customization.
    """

    model = user_models.User
    add_form = user_forms.CustomUserCreationForm
    form = user_forms.CustomUserChangeForm

    list_display = ("email", "name", "is_active", "is_staff")
    search_fields = ["email", "name"]
    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Personal Info",
            {"fields": ("name", "phone_number", "city", "profile_picture")},
        ),
        (
            "permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide"),
                "fields": (
                    "email",
                    "name",
                    "phone_number",
                    "password1",
                    "password2",
                    "city",
                    "profile_picture",
                ),
            },
        ),
    )
