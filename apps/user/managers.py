from django.contrib.auth.models import BaseUserManager

from apps.user import constants as user_constants


class UserManager(BaseUserManager):
    """
    Custom manager for User model.

    Responsibilities:
        - Validate required authentication fields
        - Normalize email addresses
        - Ensure passwords are hashed before saving
        - Enforce superuser permission requirements
    """

    def create_user(self, email, password, **kwargs):
        """
        Create and return a regular user.
        """
        if not email:
            raise ValueError(user_constants.ErrorMessages.EMAIL_REQUIRED)
        if not password:
            raise ValueError(user_constants.ErrorMessages.PASSWORD_REQUIRED)

        kwargs.setdefault("is_active", True)

        email = self.normalize_email(email).lower().strip()
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **kwargs):
        """
        Create and return a superuser.
        """
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)
        kwargs.setdefault("is_active", True)

        if kwargs.get("is_staff") is not True:
            raise ValueError(user_constants.ErrorMessages.SUPERUSER_STAFF_REQUIRED)

        if kwargs.get("is_superuser") is not True:
            raise ValueError(user_constants.ErrorMessages.SUPERUSER_REQUIRED)

        return self.create_user(email, password, **kwargs)
