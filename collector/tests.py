import os
from django.test import TestCase

from crawler.settings import BASE_DIR
from collector.parsers import mpk_krakow, mpk_wroclaw

# Create your tests here.


class ParserTests(TestCase):
    def test_krakow_single_stop(self):
        """
        Test krakow single stop parser
        """
        # read html data from given template (not from web, links change periodically)
        with open(os.path.join(BASE_DIR, 'collector', 'test_resources', 'mpk_krakow_parse_bus_stop_res.html'), 'r') as file:
            html = file.read()

        self.assertListEqual(mpk_krakow.parse_bus_stop(html), [
            ('212', 'http://rozklady.mpk.krakow.pl/?lang=PL&rozklad=20171023&linia=213__1__23'),
            ('213', 'http://rozklady.mpk.krakow.pl/?lang=PL&rozklad=20171023&linia=213__2__32'),
            ('213', 'http://rozklady.mpk.krakow.pl/?lang=PL&rozklad=20171023&linia=213__4__32'),
            ('213', 'http://rozklady.mpk.krakow.pl/?lang=PL&rozklad=20171023&linia=213__3__23')
        ])

    def test_krakow_collectnig_stop_names(self):
        with open(os.path.join(BASE_DIR, 'collector', 'test_resources', 'mpk_krakow_parse_all_stops.html'), 'r') as file:
            html = file.read()

        self.assertListEqual(mpk_krakow.get_all_stops(html)[:4], [  # checks only 4 first elements
            ('Agatowa', 'http://rozklady.mpk.krakow.pl/?lang=PL&akcja=przystanek&rozklad=20171023&przystanek=QWdhdG93YQeEeeEe'),
            ('Agencja Kraków Wschód', 'http://rozklady.mpk.krakow.pl/?lang=PL&akcja=przystanek&rozklad=20171023&przystanek=QWdlbmNqYSBLcmFrw7N3IFdzY2jDs2QeEe'),
            ('AGH / UR', 'http://rozklady.mpk.krakow.pl/?lang=PL&akcja=przystanek&rozklad=20171023&przystanek=QUdIIC8gVVIeEe'),
            ('Akacjowa', 'http://rozklady.mpk.krakow.pl/?lang=PL&akcja=przystanek&rozklad=20171023&przystanek=QWthY2pvd2EeEe')
        ])


class WroclawParserTest(TestCase):
    def test_parse_bus_stop_list(self):
        stops_list = mpk_wroclaw.parse_bus_stop_list('https://www.wroclaw.pl/wszystkie-przystanki')
        self.assertTrue(('Brodzka', 'https://www.wroclaw.pl/linie-na-przystanku-brodzka-wroclaw') in stops_list)
        self.assertTrue(('Górnicza', 'https://www.wroclaw.pl/linie-na-przystanku-gornicza-wroclaw') in stops_list)
        self.assertTrue(('Serbska', 'https://www.wroclaw.pl/linie-na-przystanku-serbska-wroclaw')in stops_list)
        self.assertTrue(('Strzegomska 56', 'https://www.wroclaw.pl/linie-na-przystanku-strzegomska-56-wroclaw') in stops_list)
        self.assertTrue(('TRZMIELOWICKA (Stacja kolejowa)', 'https://www.wroclaw.pl/linie-na-przystanku-trzmielowicka-stacja-kolejowa-wroclaw') in stops_list)
        self.assertTrue(('Zębice - Trzech Lip/Prusa', 'https://www.wroclaw.pl/linie-na-przystanku-zebice-trzech-lip-prusa-wroclaw') in stops_list)

