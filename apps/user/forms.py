from django.contrib.auth import forms

from apps.user import models as user_models


class CustomUserCreationForm(forms.UserCreationForm):
    """
    Form used in Django admin to create new users.

    This form extends Django's built-in UserCreationForm to support
    the custom User model.

    Fields:
        name (str): Full name of the user.
        email (str): Unique email address of the user.
        phone_number (str): Phone number of the user.
        city (City): Reference to the city modal for user's city.
        profile_picture (Image): Profile image uploaded by the user.
        is_staff (bool): Determines if the user can access Django admin panel.
        is_superuser (bool): Grants all permissions to the user.
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

    This form extends Django's built-in UserChangeForm to support
    updates to the custom User model.

    Fields:
        name (str): Full name of the user.
        email (str): Unique email address of the user.
        phone_number (str): Phone number of the user.
        city (City): Reference to the city modal for user's city.
        profile_picture (Image): Profile image uploaded by the user.
        is_staff (bool): Determines if the user can access Django admin panel.
        is_superuser (bool): Grants all permissions to the user.
        is_active (bool): Controls whether the user account is active.
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
