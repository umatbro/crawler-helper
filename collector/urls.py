from django.conf.urls import url, include

from collector import views

app_name = 'collector'

urlpatterns = [
    # url(regex, view, name)
    url(r'^all$', views.all_info, name='all_info'),
    url(r'^timetables/$', views.city_timetables, name='timetables'),
    url(r'^busstop/(?P<id>\d*)/?$', views.bus_stop, name='bus_stop'),
]

