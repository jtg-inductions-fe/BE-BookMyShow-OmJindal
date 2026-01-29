class UserConstants:
    """
    Centralized database-related constants for the User app.
    """

    NAME_MAX_LENGTH = 50
    PHONE_NUMBER_MAX_LENGTH = 10
    PROFILE_PICTURE_DIR = "users/"


class ValidationConstants:
    """
    Constants used for validating user input fields.
    """

    PHONE_NUMBER_REGEX = r"^\d{10}$"
    PHONE_NUMBER_ERROR_MESSAGE = "Phone number should be exactly 10 numeric digits"


class ErrorMessages:
    """
    Centralized error message constants for the User app.
    """

    EMAIL_REQUIRED = "Users must have an email address."
    PASSWORD_REQUIRED = "Password is compulsory."
    SUPERUSER_STAFF_REQUIRED = "Superuser must have is_staff=True."
    SUPERUSER_REQUIRED = "Superuser must have is_superuser=True."

    PASSWORD_MISMATCH = "Passwords do not match."
