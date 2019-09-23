from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from rest_framework import serializers

from collector.models import BusStop
from collector.models import City


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name', 'last_update']


class BusStopSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusStop
        fields = '__all__'


class CityDetailsSerializer(serializers.ModelSerializer):
    bus_stops = serializers.SerializerMethodField()

    class Meta:
        model = City
        fields = ('id', 'name', 'last_update', 'bus_stops')

    def get_bus_stops(self, obj: City):
        return BusStop.objects.filter(city=obj).values_list('name', flat=True)
