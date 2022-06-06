# Generated by Django 4.0.4 on 2022-05-27 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('Unverified', 'Unverified'), ('Verified', 'Verified'), ('Administrator', 'Aaministrtor'), ('Archived', 'Archived')], max_length=50, null='Unverified'),
            preserve_default='Unverified',
        ),
    ]