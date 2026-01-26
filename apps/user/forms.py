from django.contrib.auth import forms

from apps.user import models as user_models


class CustomUserCreationForm(forms.UserCreationForm):
    """
    Form used in Django admin to create new users.

    Ensures password hashing and validation.
    """

    class Meta:
        model = user_models.User
        fields = (
            "name",
            "email",
            "phone_number",
            "city",
            "profile_picture",
            "is_staff",
            "is_superuser",
        )


class CustomUserChangeForm(forms.UserChangeForm):
    """
    Form used in Django admin to update existing users.
    """

    class Meta:
        model = user_models.User
        fields = (
            "email",
            "name",
            "phone_number",
            "city",
            "profile_picture",
            "is_active",
            "is_staff",
            "is_superuser",
        )
