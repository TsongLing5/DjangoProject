# Generated by Django 2.1.7 on 2019-07-25 11:32

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20190707_1551'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlepost',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 25, 11, 32, 48, 441576, tzinfo=utc)),
        ),
    ]
