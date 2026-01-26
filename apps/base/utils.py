from django.http import JsonResponse


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
            {"status": "Failed", "message": "The requested resource was not found"},
            status=404,
        )
