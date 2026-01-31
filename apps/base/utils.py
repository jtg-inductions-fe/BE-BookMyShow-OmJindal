from django.http import JsonResponse

from apps.base import constants as base_constants


class ErrorHandlers:
    """
    Utility class for custom HTTP error response handlers.
    """

    @staticmethod
    def custom_404_view(request, exception=None):
        """
        Returns a standardized JSON response for 404 errors.
        """
        return JsonResponse(
            {"message": base_constants.ErrorMessages.NOT_FOUND},
            status=404,
        )


class NormalizedNameMixin:
    """
    Mixin that normalizes the 'name' field to lowercase
    and strips whitespace.
    """

    def save(self, *args, **kwargs):
        if hasattr(self, "name") and self.name:
            self.name = self.name.lower().strip()
        return super().save(*args, **kwargs)
