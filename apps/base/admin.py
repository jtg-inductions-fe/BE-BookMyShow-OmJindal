from django.contrib import admin

from apps.base import models as base_models

admin.site.register(base_models.Language)
admin.site.register(base_models.Genre)
admin.site.register(base_models.City)