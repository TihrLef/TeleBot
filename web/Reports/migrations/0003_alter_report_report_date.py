# Generated by Django 4.0.4 on 2022-04-21 20:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Reports', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='report_date',
            field=models.DateField(default=datetime.datetime.now),
        ),
    ]
