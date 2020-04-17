from django.contrib import admin

# Register your models here.
from weather.models import City, MainCities


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ["name", "id"]


@admin.register(MainCities)
class MainCitiesAdmin(admin.ModelAdmin):
    list_display = ["name", "id"]
