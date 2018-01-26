import requests
from bs4 import BeautifulSoup

from collector.models import City
from collector.parsers.city import update_city as upd_city

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
    :return: 2 element tuple (line number, link to timetable)
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

    # get info
    bus_stops_list_link = BeautifulSoup(requests.get(ZTM_HOMEPAGE).text, 'html.parser')\
        .select_one('a[title="szukaj z przystanku"]').attrs['href']
    stops_list = parse_bus_stop_list(bus_stops_list_link)
    upd_city(city, stops_list, parse_bus_stop)

