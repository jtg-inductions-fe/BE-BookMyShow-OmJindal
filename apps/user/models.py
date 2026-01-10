from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from apps.user import managers as user_manager
from apps.base.models import City, TimeStampedModel

# Validator to ensure the phone number is exactly 10 digits
phone_number_validator = RegexValidator(
    regex=r"^\d{10}$",
    message="Phone number should be exactly 10 digits",
    code="Invalid Phone number",
)


class User(TimeStampedModel, AbstractBaseUser, PermissionsMixin):
    """
    Custom User model using email as the unique identifier.
    """

    name = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(
        validators=[phone_number_validator],
        max_length=10,
        null=True,
        blank=True,
    )
    city = models.ForeignKey(
        City, on_delete=models.SET_NULL, null=True, blank=True, related_name="users"
    )
    profile_picture = models.ImageField(
        upload_to="profile_pictures/", null=True, blank=True
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = user_manager.UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "phone_number"]

    def __str__(self):
        return self.email

    def save(self):
        self.email = self.email.lower()
        return super().save()
