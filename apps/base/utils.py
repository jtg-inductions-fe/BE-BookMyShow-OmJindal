from django.http import JsonResponse

from apps.base import constants as base_constants


class CustomException:
    """
    Utility class for handling application-wide exceptions.
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
