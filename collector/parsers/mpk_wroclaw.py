from collections import defaultdict

import requests
from bs4 import BeautifulSoup

from django.utils import timezone
from collector.models import City, BusStop, Timetable

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
    :return:
    """
    pass


def update_city():
    """
    Update city:

    * save BusStops
    * delete old BusStops
    * save timetables
    :return:
    """
    pass
