import re
import requests
from bs4 import BeautifulSoup
from collections import defaultdict

from typing import List, Tuple, DefaultDict
from string import ascii_uppercase

MPK_HOMEPAGE = 'http://www.mpk.poznan.pl/'
BUS_STOPS_ALPHABETICALLY_LINK = 'http://www.mpk.poznan.pl/component/transport/?letter={}&co=letter'

LETTERS = list(ascii_uppercase) + ['Ż', 'Ś', 'Ł']
LETTERS.remove('X'); LETTERS.remove('V'); LETTERS.remove('Q')

BUS_STOP_TITLE_PATTERN = re.compile(r'^(?P<stop_name>[\w ]+) ?\([A-Z]+[A-Z0-9]+\)')


def gather_links_to_letters():
    """
    Poznan has list bus stop list but they are separated by alphabet letters.
    To parse all stops one has to check all alphabet subsites.

    :return: list with links to all sites by alphabet letters
    """
    return [BUS_STOPS_ALPHABETICALLY_LINK.format(letter) for letter in LETTERS]


def parse_bus_stop_list(link_to_bus_stop_list: str) -> DefaultDict[str, List[Tuple[str, str]]]:
    """
    Parse single bus stop and get all lines that have departures from there with link to the timetable.

    :param link_to_bus_stop_list: link to webpage with listed lines
    :return: list with 2-element tuples (line number, link to timetable)
    """
    soup = BeautifulSoup(requests.get(link_to_bus_stop_list).content.decode('utf-8'), 'html.parser')
    stops = soup.select('div#MIMMPK > ul > li')

    result = defaultdict(list)
    for stop in stops:
        try:
            text = stop.select_one('a span strong').text
            match = re.match(BUS_STOP_TITLE_PATTERN, text)
            if match:
                stop_name = match.groupdict()['stop_name']
            else:
                print('Error on {}'.format(text))
                raise KeyError
        except KeyError:
            continue
        else:
            lines = stop.select('ul li a')
            for line in lines:
                line_number = line.text
                line_link = MPK_HOMEPAGE[:-1] + line.attrs['href']
                result[stop_name].append((line_number, line_link))
    return result

