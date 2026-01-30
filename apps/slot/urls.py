from django.urls import path

from apps.slot import views as slot_views

urlpatterns = [
    path("<int:pk>/", slot_views.SlotDetailView.as_view(), name="slot-detail"),
]
