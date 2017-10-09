from django.db import models

# Create your models here.


class City(models.Model):
    name = models.CharField(max_length=30)


class BusStop(models.Model):
    city = models.ForeignKey(City)
    name = models.CharField(max_length=200, blank=True, default='')


class Timetable(models.Model):
    link = models.CharField(max_length=200)
    line_number = models.CharField(max_length=10)
    bus_stop = models.ForeignKey(BusStop)
    # add vehicle type ?
