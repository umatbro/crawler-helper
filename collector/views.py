from django.shortcuts import render
from collector.parsers import mpk_krakow
from django.http import JsonResponse
from collector.models import City, BusStop, Timetable


# Create your views here.

def update_city_view(request, city_name):
    pass


def city_timetables(request):
    """
    Fetch timetables for queried cities.

    GET method params:

    * city

    :param request:
    :return: list of city objects
    city object fields: name, lastUpdate, stops.
    `stops` field is a list with bus stops and all lines leaving from this stop.
    """
    response = []
    cities = request.GET.getlist('city')
    for city_str in cities:
        try:
            city = City.objects.get(name__iexact=city_str)
        except City.DoesNotExist:
            response.append({
                'name': city_str,
                'cityNotFound': True,
            })
        else:
            city_stops = []
            for stop in city.busstop_set.all():
                city_stops.append({stop.name: [{line.line_number: line.link} for line in stop.timetable_set.all()]})
            response.append({
                'name': city.name,
                'lastUpdate': city.last_update,
                'stops': city_stops
            })

    return JsonResponse(response, safe=False)


def all_info(request):
    response = {}
    for city in City.objects.all():
        response[city.name] = {
            bus_stop.name: {timetable.line_number: timetable.link for timetable in bus_stop.timetable_set.all()}
            for bus_stop in BusStop.objects.filter(city=city)
        }

    return JsonResponse(response)
