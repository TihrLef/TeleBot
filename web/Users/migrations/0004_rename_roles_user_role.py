# Generated by Django 4.0.4 on 2022-05-27 11:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0003_remove_user_role_user_roles'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='roles',
            new_name='role',
        ),
    ]
