from django.contrib import admin

from apps.slot import models as slot_models

admin.site.register(slot_models.Slot)
admin.site.register(slot_models.Booking)
admin.site.register(slot_models.Ticket)
