from rest_framework.routers import DefaultRouter
from apps.movie.views import MovieViewSet

router = DefaultRouter()
router.register("", MovieViewSet, basename="movies")

urlpatterns = router.urls
