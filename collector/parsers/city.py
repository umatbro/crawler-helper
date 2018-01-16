from collections import defaultdict


class CityParser:
    def __init__(self, name=''):
        self.city_name = name
        self.stops = defaultdict(list)

    def collect_info(self):
        """
        Get all information from webpage. Select parser based on city class value
        """
        pass
