import requests
from bs4 import BeautifulSoup


def parse_bus_stop(html: str) -> list:
    """
    Parse single bus stop and get all lines that have departures from there with link to the timetable

    :param html: HTML from bus stop webpage with listed lines
    :return: list with 2-element tuples (line number, link to timetable)
    """
    soup = BeautifulSoup(html, 'html.parser')
    items_list = soup.select('html body table.main tbody tr td table tbody tr')
    result = []
    for item in items_list:
        number = item.select('td')[1].text.rstrip().lstrip()
        link = item.select('td')[3].select('a')[0].get('href')
        result.append((number, link))

    return result


def get_all_stops(html: str) -> list:
    """
    From main page where all bus stops are listed get all links assigned to bus stop names

    :param html: html code from main page, where all stops are listed, http://rozklady.mpk.krakow.pl/?lang=PL&rozklad=20171023&akcja=przystanek
    :return: list with 2-element tuples (bus stop name, link to bus stop)
    """
    soup = BeautifulSoup(html, 'html.parser')
    items_list = soup.select('html body table.main tbody tr td form#main table tbody tr td a')
    result = []
    for item in items_list:
        link = item.get('href')
        name = item.select('span')[0].text.rstrip().lstrip()
        result.append((name, link))

    return result


def mpk_content(url):
    r_first = requests.get(url)
    r = requests.get(url, cookies=r_first.cookies)
    return r.text
