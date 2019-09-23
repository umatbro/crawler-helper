import requests

from bs4 import BeautifulSoup
from collector.models import City
from collector.parsers import city as city_upd

MPK_HOMEPAGE = 'https://www.wroclaw.pl/'


def parse_bus_stop_list(link: str) -> list:
    """
    From main page where all bus stops are listed get all links assigned to bus stop names

    :param link: link to page with bus stops listed
    :return: list with 2-element tuples (bus stop name, link to bus stop)
    """
    soup = BeautifulSoup(requests.get(link).content.decode('utf-8'), 'html.parser')
    elements = soup.select('article.article-schedules ul.unstyled.all-lines-list li ul.filtered-lines-list li a')

    return [(elem.text, MPK_HOMEPAGE[:-1] + elem.attrs['href']) for elem in elements]


def parse_bus_stop(link_to_bus_stop: str) -> list:
    """
    Parse bus stop page to return list of tuples (line number, link to timetable).

    :param link_to_bus_stop: link directing to page with timetables listed
    :return: 2 element tuple (line number, link to timetable)
    """
    soup = BeautifulSoup(requests.get(link_to_bus_stop).content.decode('utf-8'), 'html.parser')
    rows = soup.select('table.table.table-bordered.table-schedule tbody tr')
    bus_line_buttons = filter(lambda item: item is not None, [row.select_one('td a.btn') for row in rows])

    return [(button.text, MPK_HOMEPAGE[:-1] + button.attrs['href']) for button in bus_line_buttons]


def update_city():
    """
    Update city:

    * save BusStops
    * delete old BusStops
    * save timetables
    :return:
    """
    city, just_created = City.objects.get_or_create(name='Wrocław')
    stops_list = parse_bus_stop_list('https://www.wroclaw.pl/wszystkie-przystanki')
    city_upd.update_city(city, stops_list, parse_bus_stop)
