from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models as db_models

from apps.base import models as base_models
from apps.user import constants as user_constants
from apps.user import managers as user_manager

# Validator to ensure the phone number is exactly 10 digits
phone_number_validator = RegexValidator(
    regex=user_constants.ValidationConstants.PHONE_NUMBER_REGEX,
    message=user_constants.ValidationConstants.PHONE_NUMBER_ERROR_MESSAGE,
    code="invalid_phone_number",
)


class User(base_models.TimeStampedModel, AbstractBaseUser, PermissionsMixin):
    """
    Custom User model where email is the unique identifier for authentication.

    This model extends AbstractBaseUser to provide full control over the
    user fields and PermissionsMixin to support Django's standard
    group and permission logic.

    Attributes:
        name (str): The full name of the user.
        email (str): Unique email address, serves as the USERNAME_FIELD.
        phone_number (str): 10-digit mobile number, validated via regex.
        city (ForeignKey): Reference to the city model.
        profile_picture (ImageField): Path to the uploaded profile image.
        is_staff (bool): Boolean flag for Django admin access.
        is_active (bool): Boolean flag for user status.
    """

    name = db_models.CharField(
        max_length=user_constants.UserConstants.NAME_MAX_LENGTH, null=True, blank=True
    )
    email = db_models.EmailField(unique=True)
    phone_number = db_models.CharField(
        validators=[phone_number_validator],
        max_length=user_constants.UserConstants.PHONE_NUMBER_MAX_LENGTH,
        blank=True,
    )
    city = db_models.ForeignKey(
        base_models.City,
        on_delete=db_models.SET_NULL,
        null=True,
        blank=True,
        related_name="users",
    )
    profile_picture = db_models.ImageField(
        upload_to=user_constants.UserConstants.PROFILE_PICTURE_DIR,
        null=True,
        blank=True,
    )
    is_active = db_models.BooleanField(default=True)
    is_staff = db_models.BooleanField(default=False)

    # Custom manager responsible for user and superuser creation logic.
    objects = user_manager.UserManager()

    # Field used by Django authentication system for authentication.
    USERNAME_FIELD = "email"

    # Fields required when creating a user via createsuperuser command.
    REQUIRED_FIELDS = ["name", "phone_number"]

    def __str__(self):
        return self.email
