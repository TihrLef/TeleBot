from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
# Create your models here.

from django.db import models
from django.urls import reverse
from datetime import date
from django.urls import reverse


class User(AbstractUser):
    telegram_id = models.BigIntegerField(primary_key=True, unique=True)

    def __str__(self):
        """String for representing the Model object"""
        return self.username

    def get_absolute_url(self):
        return reverse('user-detail', args=[str(self.telegram_id)])

    def my_view(self, request):
        username = None
        if request.user.is_authenticated():
            username = request.user.username

    @property
    def get_role(self):
        if self.is_staff:
            return "Администратор"
        else:
            if self.is_active:
                return "Подтвержденный"
            else:
                return "Неподтвержденный"

    def is_verified(self):
        return self.is_active or self.is_staff

    @staticmethod
    def make_from_dict(data):
        user, created = User.objects.get_or_create(telegram_id=data.get('id', ''))
        user.first_name = data.get('first_name', '')
        user.last_name = data.get('last_name', '')
        user.username = data.get('username', '')
        user.is_active = True

        return user
