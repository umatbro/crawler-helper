from collections import defaultdict

import requests
from bs4 import BeautifulSoup

from django.utils import timezone
from collector.models import City, BusStop, Timetable

ZTM_HOMEPAGE = 'http://www.ztm.waw.pl/'


def parse_bus_stop_list(link: str) -> list:
    """
    From main page where all bus stops are listed get all links assigned to bus stop names

    :param link: link to page with bus stops listed
    :return: list with 2-element tuples (bus stop name, link to bus stop)
    """
    soup = BeautifulSoup(requests.get(link).content.decode('utf-8'), 'html.parser')
    przystanek_lists = soup.select('div.PrzystanekList')
    links = []
    for item in przystanek_lists:
        links.extend([(link.text, ZTM_HOMEPAGE + link.attrs['href']) for link in item.select('a')])

    return links


def parse_bus_stop(link_to_bus_stop: str) -> list:
    """
    Parse bus stop page to return list of tuples (line number, link to timetable).

    :param link_to_bus_stop: link directing to page with timetables listed (example:
    http://www.ztm.waw.pl/rozklad_nowy.php?c=183&l=1&a=3748)
    :return:
    """
    content = requests.get(link_to_bus_stop).content.decode('utf-8')
    soup = BeautifulSoup(content, 'html.parser')

    _ = soup.select('div.PrzystanekKierunek div.PrzystanekLineList')
    links = []
    for line in _:
        links_ = line.select('a')
        links.extend([(link.text, ZTM_HOMEPAGE + link.attrs['href']) for link in links_])

    return links


def update_city():
    """
    Update city:

    * save BusStops
    * delete old BusStops
    * save timetables
    :return:
    """
    city, just_created = City.objects.get_or_create(name='Warszawa')
    old_stops = city.busstop_set.all()

    # get info
    bus_stops_list_link = BeautifulSoup(requests.get(ZTM_HOMEPAGE).text, 'html.parser')\
        .select_one('a[title="szukaj z przystanku"]').attrs['href']
    # stops_list = list(map(lambda x: (re.sub(r'\s\(.+\)', '', x[0]), x[1]), parse_bus_stop_list(bus_stops_list_link)))
    stops_list = parse_bus_stop_list(bus_stops_list_link)
    bulk = [BusStop(name=stop_name, city=city) for stop_name, stop_link in stops_list]

    # deal with duplicate names (concat number to name like this name(1))
    names = defaultdict(lambda: 0)
    for item in bulk:
        names[item.name] += 1
        if names[item.name] > 1:
            item.name += '({})'.format(names[item.name] - 1)
    # delete old stops
    old_stops.delete()
    # save new stops
    BusStop.objects.bulk_create(bulk)

    bulk = []
    for stop_name, stop_link in stops_list:
        print('Gathering \'{}\''.format(stop_name))
        [bulk.append(Timetable(
            link=link,
            line_number=line_num,
            bus_stop=BusStop.objects.get(name=stop_name),
            last_update=timezone.now(),
        )) for line_num, link in parse_bus_stop(stop_link)]

    Timetable.objects.bulk_create(bulk)
    city.last_update = timezone.now()
    city.save()

