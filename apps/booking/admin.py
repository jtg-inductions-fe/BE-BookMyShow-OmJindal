from django.contrib import admin

from apps.booking import models as booking_models

admin.site.register(booking_models.Booking)
