# Generated by Django 4.0.4 on 2022-06-05 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0002_user_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('Verified', 'Verified'), ('Unverified', 'Unverified'), ('Administrator', 'Administrator')], max_length=50)),
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('Unverified', 'Unverified'), ('Verified', 'Verified'), ('Administrator', 'Administrator'), ('Archived', 'Archived')], max_length=50, null='Unverified'),
        ),
    ]
