from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.user import models as user_models


class CustomUserAdmin(UserAdmin):
    model = user_models.User

    list_display = ("email", "name", "is_active", "is_staff")
    list_filter = ["is_staff", "is_superuser"]
    search_fields = ["email", "name"]

    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("name", "phone_number")}),
        (
            "permissions",
            {"fields": ("is_active", "is_staff", "groups", "user_permissions")},
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "name",
                    "phone_number",
                    "password1",
                    "password2",
                    "is_superuser",
                    "is_staff",
                )
            },
        ),
    )

    def save_model(self, request, obj, form, change):
        if form.cleaned_data.get("password1") and not change:
            obj.set_password(form.cleaned_data["password1"])
        super().save_model(request, obj, form, change)


admin.site.register(user_models.User, CustomUserAdmin)
