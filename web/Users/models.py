from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
# Create your models here.

from django.db import models
from django.urls import reverse 
from datetime import date
from django.urls import reverse
	

class User(AbstractUser):
    personal_token = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this particular book across whole library")
    def __str__(self):
        """String for representing the Model object"""
        return self.username
    def get_absolute_url(self):
        """Returns the url to access a particular book instance."""
        return reverse('person-detail', args=[str(self.id)])
    
    def my_view(self, request):
        username = None
        if request.user.is_authenticated():
            username = request.user.username
            
            