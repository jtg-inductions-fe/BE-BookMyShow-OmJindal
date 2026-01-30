from rest_framework.routers import SimpleRouter

from apps.cinema import views as cinema_views

router = SimpleRouter()
router.register("", cinema_views.CinemaViewSet, basename="cinemas")
urlpatterns = router.urls
