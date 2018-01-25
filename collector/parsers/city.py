from typing import Callable, List, Tuple
from collector.models import City, Timetable, BusStop
from collections import defaultdict

from django.utils import timezone


class CityParser:
    def __init__(self, name=''):
        self.city_name = name
        self.stops = defaultdict(list)

    def collect_info(self):
        """
        Get all information from webpage. Select parser based on city class value
        """
        pass


def update_city(city: City, stops_list: List[Tuple[str, str]], parse_bus_stop_function: Callable[[str], list]) -> None:
    """
    Update city:

    * save BusStops
    * delete old BusStops
    * save timetables
    """
    names = defaultdict(lambda: 0)
    for i, (bus_stop_name, bus_stop_link) in enumerate(stops_list):
        # if bus stops names are the same  this  will append some number after their name
        names[bus_stop_name] += 1
        if names[bus_stop_name] > 2:
            bus_stop_name += '({})'.format(names[bus_stop_name] - 1)

        # save bus stop to database
        bus_stop_model, just_created = BusStop.objects.get_or_create(city=city, name=bus_stop_name)
        print('Gathering \'{}\' ({}%)'.format(bus_stop_name, (i+1)*100//len(stops_list)))  # print progress
        bulk = [Timetable(
            bus_stop=bus_stop_model,
            link=timetable_link,
            line_number=line_number,
            last_update=timezone.now()
        ) for line_number, timetable_link in parse_bus_stop_function(bus_stop_link)]

        # if bus stop model existed before - clear all timetables assigned to it
        if not just_created:
            bus_stop_model.timetable_set.all().delete()

        Timetable.objects.bulk_create(bulk)
