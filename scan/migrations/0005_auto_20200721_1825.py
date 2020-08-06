# Generated by Django 3.0.8 on 2020-07-21 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scan', '0004_auto_20200721_1809'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scandetailstable',
            name='image',
        ),
        migrations.AddField(
            model_name='scandetailstable',
            name='scanDetailImageRaw',
            field=models.ImageField(blank=True, null=True, upload_to='media/scan/'),
        ),
        migrations.AddField(
            model_name='scandetailstable',
            name='scanDetailImageUrl',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
