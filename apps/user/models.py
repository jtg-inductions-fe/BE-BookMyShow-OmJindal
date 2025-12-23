from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .managers import UserManager

# Validator to ensure the phone number is exactly 10 digits
phone_number_validator = RegexValidator(
    regex=r"^\d{10}$",
    message="Phone number should be exactly 10 digits",
    code="Invalid Phone number",
)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Represents a user for the system.

    Attributes:
        name (str) : The full name of the user.
        email (str) : The unique email address used for login.
        phone_number (str) : The unique 10-digit contact number.
        is_active (bool) : Designates whether this user is active.
        is_staff (bool) : Designates whether the user can log into the admin site.
    """

    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(
        unique=True, validators=[phone_number_validator], max_length=10
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["password"]

    def __str__(self):
        return self.name
