from rest_framework.routers import SimpleRouter

from apps.booking import views as booking_views

router = SimpleRouter()
router.register("", booking_views.BookingViewSet, basename="booking")
urlpatterns = router.urls
