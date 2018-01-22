from django.db import models

# Create your models here.


class City(models.Model):
    name = models.CharField(max_length=30)
    last_update = models.DateTimeField(null=True)

    def __str__(self):
        return '{}({}, id: {})'.format(self.__class__.__name__, self.name, self.id)

    def __repr__(self):
        return '<{}: ({}, id: {})>'.format(self.__class__.__name__, self.name, self.id)


class BusStop(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, blank=True, default='')

    class Meta:
        unique_together = ('city', 'name')

    def __str__(self):
        return 'BusStop({}, {})'.format(self.name, self.city.name)


class Timetable(models.Model):
    link = models.CharField(max_length=200, null=True)
    line_number = models.CharField(max_length=10, null=True)
    bus_stop = models.ForeignKey(BusStop, on_delete=models.CASCADE)
    last_update = models.DateTimeField(null=True)
