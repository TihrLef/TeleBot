# Generated by Django 4.0.4 on 2022-05-27 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Projects', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.TextField(max_length=200, unique=True),
        ),
    ]
