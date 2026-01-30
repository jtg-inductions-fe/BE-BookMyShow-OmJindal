from rest_framework.routers import SimpleRouter

from apps.movie import views as movie_views

router = SimpleRouter()
router.register("", movie_views.MovieViewSet, basename="movie")
urlpatterns = router.urls
