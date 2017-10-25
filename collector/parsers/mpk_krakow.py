from bs4 import BeautifulSoup


def parse_bus_stop(html: str) -> list:
    """
    Parse single bus stop and get all lines that have departures from there with link to the timetable

    :param html: HTML from bus stop webpage with listed lines
    :return: list with 2-element tuples (line number, link to timetable)
    """
    pass


def get_all_stops(html: str) -> list:
    """
    From main page where all bus stops are listed get all links assigned to bus stop names

    :param html: html code from main page, where all stops are listed, http://rozklady.mpk.krakow.pl/?lang=PL&rozklad=20171023&akcja=przystanek
    :return: list with 2-element tuples (bus stop name, link to bus stop)
    """
    pass
