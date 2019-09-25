from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from rest_framework import status as s
from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api2 import services
from api2.serializers import CityDetailsSerializer
from api2.serializers import CityListSerializer
from api2.serializers import CitySerializer
from api2.serializers import GroupSerializer
from api2.serializers import UserSerializer
from api2.tasks import send_email_with_dump_task
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


class GetDumpView(APIView):
    def post(self, request: Request):
        serializer = CityListSerializer(data=request.data)
        if serializer.is_valid():
            cities = serializer.validated_data.get('cities')
            email = serializer.validated_data.get('email')
            _, errors = services.get_cities(cities)

            send_email_with_dump_task.delay(email, cities)
            # send_email_with_dump_task(email, cities)

            return Response({
                'message': 'Email with dump will be sent shortly.',
                'errors': errors,
            })
        return Response(serializer.errors, status=s.HTTP_400_BAD_REQUEST)
