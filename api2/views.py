from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from rest_framework.generics import RetrieveAPIView

from api2.serializers import CityDetailsSerializer
from api2.serializers import CitySerializer
from api2.serializers import GroupSerializer
from api2.serializers import UserSerializer
from collector.models import City


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CitiesView(ListAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer


class CityView(RetrieveAPIView):
    serializer_class = CityDetailsSerializer
    queryset = City.objects.all()
    lookup_field = 'id'
