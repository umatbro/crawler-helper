from django.contrib import admin

from collector import models


@admin.register(models.City)
class CityAdmin(admin.ModelAdmin):
    pass


@admin.register(models.TimetableLink)
class TimetableAdmin(admin.ModelAdmin):
    autocomplete_fields = ('bus_stop', )
    list_display = ('bus_stop', 'line_number', 'last_update')


@admin.register(models.BusStop)
class BusStopAdmin(admin.ModelAdmin):
    search_fields = ('name', 'city__name',)
