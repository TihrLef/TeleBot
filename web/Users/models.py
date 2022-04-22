from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
# Create your models here.

from django.db import models
from django.urls import reverse 
from datetime import date
from django.urls import reverse
	

class User(AbstractUser):
	personal_token = models.UUIDField(default=uuid.uuid4, help_text="Unique ID for this particular book across whole library")
	telegram_id = models.BigIntegerField(primary_key=True, unique = True)
	def __str__(self):
		"""String for representing the Model object"""
		return self.username
	def get_absolute_url(self):
		return reverse('user-detail', args=[str(self.telegram_id)])
    
	def my_view(self, request):
		username = None
		if request.user.is_authenticated():
			username = request.user.username
