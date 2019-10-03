import os

from django.core.management import call_command

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crawler.settings')
app = Celery('crawler')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task
def update_db():
    call_command('updatedb')


app.conf.beat_schedule = {
    'update_db': {
        'task': 'crawler.celery_cfg.update_db',
        'schedule': crontab(day_of_week='*', hour='0,12', minute='0'),
    },
}
