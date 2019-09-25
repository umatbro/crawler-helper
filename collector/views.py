from django.http import JsonResponse

from collector.models import BusStop
from collector.models import City


def update_city_view(request, city_name):
    pass


def city_timetables(request):
    """
    Fetch timetables for queried cities.

    GET method params:

    * city
    * onlyIds - if this flag is set to 'true' it will return only bus stops ids from the database

    :param request:
    :return: list of city objects
    city object fields: name, lastUpdate, stops.
    `stops` field is a list with bus stops and all lines leaving from this stop.
    """
    response = {}
    cities_j = []
    cities = request.GET.getlist('city')
    only_ids = request.GET.get('onlyIds', '')
    only_ids = True if only_ids.lower() == 'true' else False

    for city_str in cities:
        try:
            city = City.objects.get(name__iexact=city_str)
        except City.DoesNotExist:
            cities_j.append({
                'name': city_str,
                'cityNotFound': True,
            })
        else:
            city_stops = []
            for stop in city.busstop_set.all():
                city_stops.append(
                    {stop.name: [{line.line_number: line.link} for line in stop.timetablelink_set.all()]}
                    if not only_ids else stop.id
                )
            cities_j.append({
                'name': city.name,
                'lastUpdate': city.last_update,
                'stops': city_stops
            })
    response['cities'] = cities_j
    return JsonResponse(response)


def all_info(request):
    response = {}
    for city in City.objects.all():
        response[city.name] = {
            bus_stop.name: {timetable.line_number: timetable.link for timetable in bus_stop.timetablelink_set.all()}
            for bus_stop in BusStop.objects.filter(city=city)
        }

    return JsonResponse(response)


def bus_stop(request, id):
    if not id:
        return JsonResponse({
            'error': True,
            'message': 'You have to provide bus stop number. Example: /api/busstops/42',
        }, status=500)
    id = int(id)
    bus_stop = BusStop.objects.get(id=id)
    return JsonResponse({
        'name': bus_stop.name,
        'timetables': [{line.line_number: line.link} for line in bus_stop.timetablelink_set.all()]
    })
