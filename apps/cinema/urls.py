from rest_framework.routers import DefaultRouter

from apps.cinema.views import CinemaViewSet

router = DefaultRouter()
router.register("", CinemaViewSet, basename="cinemas")
urlpatterns = router.urls
