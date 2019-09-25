from django.test import TestCase

from api2 import services
from collector.models import City


class TestGetCities(TestCase):
    def setUp(self):
        self.krakow = City.objects.create(name='Kraków')
        self.warszawa = City.objects.create(name='Warszawa')
        self.wroclaw = City.objects.create(name='Wrocław')
        self.koln = City.objects.create(name='Köln')

    def test_get_cities(self):
        cities, errors = services.get_cities(['krakow', 'koln', 'gdansk'])
        self.assertListEqual(cities, [self.krakow, self.koln])
        self.assertIn('gdansk', errors)
