import base64
import json
from typing import Dict
from typing import List
from typing import Tuple

from django.conf import settings
from sendgrid import Attachment
from sendgrid import FileContent
from sendgrid import FileName
from sendgrid import FileType
from sendgrid import Mail
from sendgrid import SendGridAPIClient

from api2.serializers import CityDumpSerializer
from collector.models import City


def get_dump(cities: List[City]) -> List[dict]:
    result = []
    for city in cities:
        result.append(CityDumpSerializer(city).data)

    return result


def get_cities(cities: List[str]) -> Tuple[List[City], Dict[str, str]]:
    """
    Get list of city models given the list of strings.

    :param cities: list of city names to query
    :return: tuple - first element is list of found city models, second element is a dict containing errors: if
    some city name from `cities` list could not be found, it will be present in this dict as a key.
    """
    city_models = []
    errors = {}
    for city in cities:
        try:
            city_models.append(City.objects.get(name__unaccent__iexact=city))
        except City.DoesNotExist:
            errors[city] = 'Cannot find this city in our database'

    return city_models, errors


def send_email_with_dump(email: str, dump: dict):
    message = Mail(
        from_email='admin@umatbro.gq',
        to_emails=email,
        subject='Data dump',
        plain_text_content='Your dump is in the attachment.'
    )

    attachment = Attachment()
    encoded = base64.b64encode(json.dumps(dump).encode('utf-8')).decode()
    attachment.file_content = FileContent(encoded)
    attachment.file_type = FileType('application/json')
    attachment.file_name = FileName('dump.json')
    message.attachment = attachment
    sendgrid_client = SendGridAPIClient(settings.SENDGRID_API_KEY)
    response = sendgrid_client.send(message)

    return response
