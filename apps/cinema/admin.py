from django.contrib import admin

from apps.cinema import models as cinema_models

admin.site.register(cinema_models.Cinema)
admin.site.register(cinema_models.Seat)
