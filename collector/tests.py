import os
import traceback
from copy import deepcopy
from unittest import skip

from django.test import TestCase

from collector.models import City
from collector.models import TimetableLink
from collector.parsers import mpk_krakow
from collector.parsers import mpk_poznan
from collector.parsers import mpk_wroclaw
from collector.parsers import ztm_warszawa
from crawler.settings import BASE_DIR


@skip
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


@skip
class WroclawParserTest(TestCase):
    def test_parse_bus_stop_list(self):
        stops_list = mpk_wroclaw.parse_bus_stop_list('https://www.wroclaw.pl/wszystkie-przystanki')
        self.assertTrue(('Brodzka', 'https://www.wroclaw.pl/linie-na-przystanku-brodzka-wroclaw') in stops_list)
        self.assertTrue(('Górnicza', 'https://www.wroclaw.pl/linie-na-przystanku-gornicza-wroclaw') in stops_list)
        self.assertTrue(('Serbska', 'https://www.wroclaw.pl/linie-na-przystanku-serbska-wroclaw')in stops_list)
        self.assertTrue(('Strzegomska 56', 'https://www.wroclaw.pl/linie-na-przystanku-strzegomska-56-wroclaw') in stops_list)
        self.assertTrue(('TRZMIELOWICKA (Stacja kolejowa)', 'https://www.wroclaw.pl/linie-na-przystanku-trzmielowicka-stacja-kolejowa-wroclaw') in stops_list)
        self.assertTrue(('Zębice - Trzech Lip/Prusa', 'https://www.wroclaw.pl/linie-na-przystanku-zebice-trzech-lip-prusa-wroclaw') in stops_list)


@skip
class UpdateTester(TestCase):
    def test_krakow_update_twice(self):
        try:
            mpk_krakow.update_city()
            city = City.objects.get(name='Kraków')
            krak_busstops_before = city.busstop_set.count()
            krak_timetables_before = TimetableLink.objects.filter(bus_stop__city=city).count()
            krakow_prev_date = deepcopy(city.last_update)
            mpk_krakow.update_city()

        except Exception as e:
            traceback.print_exc()
            self.fail(e)
        else:
            city.refresh_from_db()
            self.assertNotEqual(0, city.busstop_set.count())
            self.assertNotEqual(0, TimetableLink.objects.filter(bus_stop__city=city).count())
            self.assertEqual(krak_busstops_before, city.busstop_set.count())
            self.assertEqual(krak_timetables_before, TimetableLink.objects.filter(bus_stop__city=city).count())
            self.assertGreater(city.last_update, krakow_prev_date)

    def test_wwa_update_twice(self):
        try:
            ztm_warszawa.update_city()
            city = City.objects.get(name='Warszawa')
            wwa_busstops_before = city.busstop_set.count()
            wwa_timetables_before = TimetableLink.objects.filter(bus_stop__city=city).count()
            wwa_prev_date = deepcopy(city.last_update)
            ztm_warszawa.update_city()

        except Exception as e:
            traceback.print_exc()
            self.fail(e)
        else:
            city.refresh_from_db()
            self.assertNotEqual(0, city.busstop_set.count())
            self.assertNotEqual(0, TimetableLink.objects.filter(bus_stop__city=city).count())
            self.assertEqual(wwa_busstops_before, city.busstop_set.count())
            self.assertEqual(wwa_timetables_before, TimetableLink.objects.filter(bus_stop__city=city).count())
            self.assertGreater(city.last_update, wwa_prev_date)

    def test_wroc_update_twice(self):
        try:
            mpk_wroclaw.update_city()
            city = City.objects.get(name='Wrocław')
            wroc_busstops_before = city.busstop_set.count()
            wroc_timetables_before = TimetableLink.objects.filter(bus_stop__city=city).count()
            wroc_prev_date = deepcopy(city.last_update)
            mpk_wroclaw.update_city()

        except Exception as e:
            traceback.print_exc()
            self.fail(e)
        else:
            city.refresh_from_db()
            self.assertNotEqual(0, city.busstop_set.count())
            self.assertNotEqual(0, TimetableLink.objects.filter(bus_stop__city=city).count())
            self.assertEqual(wroc_busstops_before, city.busstop_set.count())
            self.assertEqual(wroc_timetables_before, TimetableLink.objects.filter(bus_stop__city=city).count())
            self.assertGreater(city.last_update, wroc_prev_date)

    def test_poznan_update_twice(self):
        try:
            mpk_poznan.update_city()
            city = City.objects.get(name='Poznań')
            poznan_busstops_before = city.busstop_set.count()
            poznan_timetables_before = TimetableLink.objects.filter(bus_stop__city=city).count()
            poznan_prev_date = deepcopy(city.last_update)
            mpk_poznan.update_city()

        except Exception as e:
            traceback.print_exc()
            self.fail(e)
        else:
            city.refresh_from_db()
            self.assertNotEqual(0, city.busstop_set.count())
            self.assertNotEqual(0, TimetableLink.objects.filter(bus_stop__city=city).count())
            self.assertEqual(poznan_busstops_before, city.busstop_set.count())
            self.assertEqual(poznan_timetables_before, TimetableLink.objects.filter(bus_stop__city=city).count())
            self.assertGreater(city.last_update, poznan_prev_date)

        alphabet = deepcopy(mpk_poznan.LETTERS)
        for stop in city.busstop_set.all():
            try:
                alphabet.remove(stop.name[0])
            except ValueError:
                continue

        if alphabet:
            self.fail('Not all alphabet letters captured.\nMissing letters: {}'.format(alphabet))
