class UserConstants:
    """
    Database configuration for the User app.
    """

    NAME_MAX_LENGTH = 50
    PHONE_NUMBER_MAX_LENGTH = 10
    PROFILE_PICTURE_DIR = "users/"


class ValidationConstants:
    """
    Constants for validation.
    """

    PHONE_NUMBER_REGEX = r"^\d{10}$"
    PHONE_NUMBER_ERROR_MESSAGE = "Phone number should be exactly 10 numeric digits"


class ErrorMessages:
    """
    Constants for defining errors.
    """

    EMAIL_REQUIRED = "Users must have an email address."
    PASSWORD_REQUIRED = "Password is compulsory."
    SUPERUSER_STAFF_REQUIRED = "Superuser must have is_staff=True."
    SUPERUSER_REQUIRED = "Superuser must have is_superuser=True."

    EMAIL_EXISTS = "A user with this email already exists."
    PASSWORD_MISMATCH = "Passwords do not match."
    FIELD_NOT_ALLOWED = "This field is not allowed."
