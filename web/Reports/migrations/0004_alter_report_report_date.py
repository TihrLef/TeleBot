# Generated by Django 4.0.4 on 2022-05-27 10:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Reports', '0003_alter_report_report_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='report_date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
