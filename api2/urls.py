from django.conf.urls import include
from django.urls import path
from rest_framework import routers

from api2 import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth', include('rest_framework.urls', namespace='rest_framework')),
    path('cities/', views.CitiesView.as_view(), name='cities'),
    path('cities/<int:id>', views.CityView.as_view(), name='city-details'),
    path('get-dump/', views.GetDumpView.as_view(), name='get-dump'),
]
