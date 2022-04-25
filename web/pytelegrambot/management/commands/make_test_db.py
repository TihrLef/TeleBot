import datetime

from django.core.management.base import BaseCommand

from Users.models import User
from Projects.models import Project
from Reports.models import Report


class Command(BaseCommand):
    help = 'Заполняет БД тестовыми данными'

    def handle(self, *args, **options):
        # Test USERS
        u1 = User.objects.create(
            username='timofone',
            first_name='Timofey',
            last_name='Bobylkov',
            telegram_id='608909090',
            is_active=True
        )

        u2 = User.objects.create(
            username='kdavovadk',
            first_name='David',
            last_name='Kosnevich',
            telegram_id='373417858',
            is_active=True
        )

        u3 = User.objects.create(
            username='snoruBe6alo',
            first_name='Marat',
            last_name='Garifullin',
            telegram_id='446713531',
            is_active=True
        )

        users = [u1, u2, u3]

        # projects
        p1 = Project.objects.create(
            name='BOT',
            responsible_user=u1,
            end_date=datetime.date(2022,5,25)
        )

        for u in users:
            p1.users.add(u)

        p2 = Project.objects.create(
            name='WEB',
            responsible_user=u2,
        )

        for u in users[1:]:
            p2.users.add(u)
        # reports
        for user in users:
            r = Report.objects.create(
                user=user,
                project=p1,
                message='Сделал что-то на проекте , моё имя: ' + user.first_name
            )
