import os
import traceback
import logging

from django.core.management.base import BaseCommand

from crawler.settings import BASE_DIR
from collector.parsers import mpk_krakow, mpk_wroclaw, mpk_poznan, ztm_warszawa


MODULES = {
    'kraków': mpk_krakow,
    'wrocław': mpk_wroclaw,
    'poznań': mpk_poznan,
    'warszawa': ztm_warszawa
}

logging.basicConfig(
    format='%(asctime)s %(levelname)s: %(message)s',
    # datefmt='%m/%d/%Y %I:%M:%S %p',
    filename=os.path.join(BASE_DIR, 'update.log'),
    level=logging.INFO,
)


class Command(BaseCommand):
    help = 'Update application data. This command parses websites and stores results in project\'s database'

    def add_arguments(self, parser):
        parser.add_argument('city_name', nargs='*', type=str)

        # optional arguments
        parser.add_argument('--log', help='log actions to a file', action='store_true')

    def handle(self, *args, **options):
        city_names = [city_name for city_name in options['city_name']] \
            if options.get('city_name', False) else \
            [city_name for city_name in MODULES.keys()]  # if no city names were provided, acquire them from database

        if options['log']:
            logging.info('Started update for cities: {}'.format(city_names))

        try:
            # update each city
            for city_name in city_names:  # type: str
                try:
                    module = MODULES[city_name.lower()]
                except KeyError:  # city not implemented
                    err_msg = 'City {} cannot be updated, it is not implemented'.format(city_name)
                    if options['log']:
                        logging.error(err_msg)
                    self.stdout.write(self.style.WARNING(
                        err_msg
                    ))
                else:
                    try:
                        module.update_city()
                    except Exception:  # any unexpected error
                        err_msg = 'Error updating {}'.format(city_name.title())
                        if options['log']:
                            logging.exception(err_msg)
                        traceback.print_exc()
                        self.stdout.write(self.style.ERROR(err_msg))
                    else:
                        msg = 'Successfully updated {}'.format(city_name.title())
                        if options['log']:
                            logging.info(msg)
                        self.stdout.write(self.style.SUCCESS(
                            msg
                        ))
        except KeyboardInterrupt:
            if options['log']:
                logging.warning('Update {} stopped by user (KeyboardInterrupt)'.format(city_name.title()))
