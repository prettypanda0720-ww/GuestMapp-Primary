# Generated by Django 3.0.8 on 2020-07-20 18:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scan', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='scandetailstable',
            table='scan_details_table',
        ),
        migrations.AlterModelTable(
            name='scantable',
            table='scan_table',
        ),
    ]
