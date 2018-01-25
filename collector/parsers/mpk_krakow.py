import requests
from bs4 import BeautifulSoup

from django.utils import timezone
from collector.models import City, BusStop, Timetable

MPK_HOMEPAGE = 'http://rozklady.mpk.krakow.pl/'


def parse_bus_stop(html: str) -> list:
    """
    Parse single bus stop and get all lines that have departures from there with link to the timetable.

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


def collect_all_info():
    """
    Collects all info from Krakow and save to database.

    :return:
    """
    city, created = City.objects.get_or_create(name='Kraków')
    if not created:
        for bus_stop in city.busstop_set.all():
            bus_stop.delete()

    main_page = requests.get(MPK_HOMEPAGE)
    mp_soup = BeautifulSoup(main_page.text, 'html.parser')
    label = mp_soup.find('label', {'class': 'label_submit', 'title': ' Przystanki '})
    link = label.select('a')[0].get('href')
    result = {}
    for stop_name, stop_link in get_all_stops(mpk_content(link, main_page.cookies)):
        print('Gathering \'{}\''.format(stop_name))
        result[stop_name] = parse_bus_stop(mpk_content(stop_link, main_page.cookies))

    city.last_update = timezone.now()
    city.save()
    return result


def collect_bulks() -> list:
    """
    Save BusStops.
    Create bulk with Timetable objects.

    :return: bulk with timetable objects
    """
    city, created = City.objects.get_or_create(name='Kraków')
    if not created:
        city.busstop_set.all().delete()

    timetable_bulk = []

    # parse html contents
    main_page = requests.get(MPK_HOMEPAGE)
    mp_soup = BeautifulSoup(main_page.content.decode('utf-8'), 'html.parser')
    label = mp_soup.find('label', {'class': 'label_submit', 'title': ' Przystanki '})
    link = label.select('a')[0].get('href')

    # create bulk
    for stop_name, stop_link in get_all_stops(mpk_content(link, main_page.cookies)):
        bus_stop = BusStop(city=city, name=stop_name)
        bus_stop.save()

        for line_number, link in parse_bus_stop(mpk_content(stop_link, main_page.cookies)):
            timetable_bulk.append(Timetable(
                bus_stop=bus_stop,
                line_number=line_number,
                link=link,
                last_update=timezone.now()
            ))
        print('Gathered \'{}\''.format(stop_name))

    return timetable_bulk


def mpk_content(url, cookies=None):
    """
    Get HTML contents of crawler-protected webpage.
    Do first connection for cookies, to try again with sending cookies in request.

    :param url: site adress
    :param cookies: cookies object
    :return: HTML code of given url
    """
    r_first = requests.get(url)
    if cookies is None:
        cookies = r_first.cookies
    r = requests.get(url, cookies=cookies)
    return r.content.decode('utf-8')


if __name__ == '__main__':
    x = collect_all_info()

    print(x)
