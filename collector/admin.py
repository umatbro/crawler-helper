from django.contrib import admin

from collector import models


@admin.register(models.City)
class CityAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Timetable)
class TimetableAdmin(admin.ModelAdmin):
    pass


@admin.register(models.BusStop)
class BusStopAdmin(admin.ModelAdmin):
    pass
