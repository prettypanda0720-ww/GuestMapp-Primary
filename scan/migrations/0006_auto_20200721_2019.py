# Generated by Django 3.0.8 on 2020-07-21 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scan', '0005_auto_20200721_1825'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scandetailstable',
            name='scanDetailImageRaw',
            field=models.ImageField(blank=True, null=True, upload_to='scan/'),
        ),
        migrations.AlterField(
            model_name='scantable',
            name='scanImageRaw',
            field=models.ImageField(blank=True, null=True, upload_to='scan/'),
        ),
    ]
