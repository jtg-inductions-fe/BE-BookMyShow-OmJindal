from django.http import JsonResponse
from rest_framework.generics import ListAPIView

from apps.base.models import Language, Genre, City
from apps.base.serializers import LanguageSerializer, GenreSerializer, CitySerializer


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


class LanguageListView(ListAPIView):
    """
    API view to retrieve the list of all available languages.
    """

    queryset = Language.objects.all()
    serializer_class = LanguageSerializer


class GenreListView(ListAPIView):
    """
    API view to retrieve the list of all available genres.
    """

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CityListView(ListAPIView):
    """
    API view to retrieve the list of all available cities.
    """

    queryset = City.objects.all()
    serializer_class = CitySerializer
