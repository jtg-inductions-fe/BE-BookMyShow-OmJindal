from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from apps.user.models import User


class CustomUserCreationForm(UserCreationForm):
    """
    Form used in Django admin to create new users.

    Ensures password hashing and validation.
    """

    class Meta:
        model = User
        fields = ("email", "name", "phone_number")


class CustomUserChangeForm(UserChangeForm):
    """
    Form used in Django admin to update existing users.
    """

    class Meta:
        model = User
        fields = (
            "email",
            "name",
            "phone_number",
            "profile_picture",
            "is_active",
            "is_staff",
            "is_superuser",
        )
