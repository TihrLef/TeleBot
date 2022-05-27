from django.db import models
from Users.models import User
from datetime import datetime, date
from django.urls import reverse    
# Create your models here.
class Project(models.Model):
	name = models.TextField(unique = True, max_length=200)
	start_date = models.DateField(default = datetime.now, null=True, blank=True)
	end_date = models.DateField(null=True, blank=True)
	users = models.ManyToManyField(User)
	responsible_user = models.ForeignKey(User, related_name="responsible", on_delete=models.SET_NULL, null=True)
    
	def __str__(self):
		"""String for representing the Model object."""
		return self.name

	def get_absolute_url(self):
		"""Returns the url to access a particular book instance."""
		return reverse('project-detail', args=[str(self.id)])
	def get_change_url(self):
		return reverse('project-change', args=[str(self.id)])

	def status(self):
		if not self.start_date or date.today()< self.start_date:
			return 'Не начался'
		if self.end_date is None or self.start_date <= date.today() < self.end_date:
			return 'В процессе'
		if date.today() >= self.end_date:
			return 'Завершился'