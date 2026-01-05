from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.user.models import User
from apps.user.forms import CustomUserChangeForm, CustomUserCreationForm


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Custom admin configuration for User model.

    Handles user creation, updates, permissions,
    and admin interface customization.
    """

    model = User
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

    list_display = ("email", "name", "is_active", "is_staff")
    search_fields = ["email", "name"]
    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("name", "phone_number")}),
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
                ),
            },
        ),
    )
