from django.http import JsonResponse


class CustomException:
    @staticmethod
    def custom_404_view(request, exception=None):
        return JsonResponse(
            {"status": "Failed", "message": "The requested resource was not found"},
            status=404,
        )

    @staticmethod
    def custom_500_view(request):
        return JsonResponse(
            {"status": "Failed", "message": "Internal Server Error"}, status=500
        )
