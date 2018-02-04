from django.core.management.base import BaseCommand, CommandError

from collector.models import City
from collector.parsers import mpk_krakow, mpk_wroclaw, mpk_poznan, ztm_warszawa


MODULES = {
    'kraków': mpk_krakow,
    'wrocław': mpk_wroclaw,
    'poznań': mpk_poznan,
    'warszawa': ztm_warszawa
}


class Command(BaseCommand):
    help = 'Update application data. This command parses webpages'

    def add_arguments(self, parser):
        parser.add_argument('city_name', nargs='*', type=str)

    def handle(self, *args, **options):
        city_names = [city_name for city_name in options['city_name']] \
            if options.get('city_name', False) else \
            [city_name for city_name in MODULES.keys()]  # if no city names were provided, acquire them from database

        print(city_names)
        for city_name in city_names:  # type: str
            try:
                module = MODULES[city_name.lower()]
            except KeyError:
                self.stdout.write(self.style.WARNING(
                    'City {} cannot be updated, it is not implemented'.format(city_name)
                ))
            else:
                try:
                    module.update_city()
                except Exception:
                    self.stdout.write(self.style.ERROR('Error updating {}'.format(city_name.title())))
                else:
                    self.stdout.write(self.style.SUCCESS(
                        'Successfully updated {}'.format(city_name.title())
                    ))
