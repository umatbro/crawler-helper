from time import sleep
from typing import List

from django.conf import settings

from api2 import services
from api2.services import send_email_with_dump
from celery import shared_task


@shared_task
def send_email_with_dump_task(email: str, cities: List[str]):
    city_models, _ = services.get_cities(cities)
    dump = services.get_dump(city_models)

    sleep(settings.SEND_DUMP_DELAY_SECONDS)
    return send_email_with_dump(email, dump)
