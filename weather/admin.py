from django.contrib import admin

# Register your models here.
from weather.models import City


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ["name"]