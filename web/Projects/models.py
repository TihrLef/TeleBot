from django.db import models
from Users.models import User
from datetime import datetime    
# Create your models here.
class Project(models.Model):
    
    
	name = models.CharField(unique = True, max_length=200)
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

	def status(self):
		if datetime.now < self.start_date:
			return 'Waiting for start'
		if self.end_date is None or self.start_date <= datetime.now() < self.end_date:
			return 'In progress'
		if datetime.now >= self.end_date:
			return 'Finished'
        
 