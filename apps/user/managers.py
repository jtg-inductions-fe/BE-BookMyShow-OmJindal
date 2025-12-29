from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    """
    Custom manager to handle user creation logic.

    Methods:
        create_user: Handles standard user registration with a compulsory password and email.
        create_superuser: Handles admin account creation with all permission flags.
    """

    def create_user(self, email, password, **kwargs):
        if not email:
            raise ValueError("Users must have an email address.")
        if not password:
            raise ValueError("Password is compulsory.")

        user = self.model(email=self.normalize_email(email), **kwargs)

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)
        kwargs.setdefault("is_active", True)

        return self.create_user(email, password, **kwargs)
