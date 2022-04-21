from django.db import models
from Users.models import User
from Projects.models import Project 
from datetime import datetime 

class Report(models.Model):
	user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True)
	report_date = models.DateField(default = datetime.now)
	message = models.TextField(max_length=1000, help_text="Write any additional comments")
	def __str__(self):
		"""String for representing the Model object."""
		return '%s:, %s' % (self.user, self.project)