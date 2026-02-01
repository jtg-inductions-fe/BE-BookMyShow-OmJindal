from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    """
    Custom manager for User model.

    Handles user and superuser creation.
    """

    def create_user(self, email, password, **kwargs):
        """
        Create and return a regular user.
        """
        if not email:
            raise ValueError("Users must have an email address.")
        if not password:
            raise ValueError("Password is compulsory.")

        email = self.normalize_email(email)
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
            raise ValueError("Superuser must have is_staff=True.")

        if kwargs.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **kwargs)
