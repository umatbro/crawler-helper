# Generated by Django 2.2.5 on 2019-09-25 19:59

from django.contrib.postgres.operations import UnaccentExtension
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0003_auto_20190923_1406'),
    ]

    operations = [
        UnaccentExtension(),
    ]
