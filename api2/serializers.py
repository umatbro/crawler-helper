from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from rest_framework import serializers

from collector.models import BusStop
from collector.models import City
from collector.models import TimetableLink


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
    bus_stops = serializers.SlugRelatedField(many=True, slug_field='name', read_only=True)

    class Meta:
        model = City
        fields = ('id', 'name', 'last_update', 'bus_stops')

    # def get_bus_stops(self, obj: City):
    #     return BusStop.objects.filter(city=obj).values_list('name', flat=True)


class TimetableLinkDumpSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimetableLink
        fields = ('line_number', 'link', 'last_update')


class BusStopDumpSerializer(serializers.ModelSerializer):
    timetables_links = TimetableLinkDumpSerializer(many=True, source='timetablelink_set')

    class Meta:
        model = BusStop
        fields = ('name', 'timetables_links')


class CityDumpSerializer(serializers.ModelSerializer):
    bus_stops = BusStopDumpSerializer(many=True)

    class Meta:
        model = City
        fields = ('name', 'bus_stops')


class CityListSerializer(serializers.Serializer):
    cities = serializers.ListField(child=serializers.CharField())
    email = serializers.EmailField(required=True, allow_null=False, allow_blank=False)
