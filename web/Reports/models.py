from django.db import models
from Users.models import User
from Projects.models import Project 
from datetime import datetime, date
import datetime

class Report(models.Model):
	user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True)
	report_date = models.DateField(default = date.today)
	message = models.TextField(max_length=1000, help_text="Write any additional comments")
	def get_date(self):
		return "%s - %s" % (self.report_date, self.report_date+datetime.timedelta(weeks=1))
	def __str__(self):
		"""String for representing the Model object."""
		return '%s: %s' % (self.user, self.project)