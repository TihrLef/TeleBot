from django.test import TestCase
from Users.models import User
from Projects.models import Project 
from datetime import datetime, date
import datetime
class StatusTest(TestCase):
	@classmethod
	def setUpTestData(cls):
		Project.objects.create(name='testProject')
	
	def test_in_progress(self):
		project=Project.objects.get(id=1)
		project.start_date=date.today()-datetime.timedelta(weeks=3)
		project.end_date=date.today()+datetime.timedelta(weeks=3)
		self.assertEquals(project.status(),'In progress')
		
	def test_waiting(self):
		project=Project.objects.get(id=1)
		project.start_date=date.today()+datetime.timedelta(weeks=2)
		project.end_date=date.today()+datetime.timedelta(weeks=3)
		self.assertEquals(project.status(),'Waiting for start')
		
		
	def test_finished(self):
		project=Project.objects.get(id=1)
		project.start_date=date.today()-datetime.timedelta(weeks=3)
		project.end_date=date.today()-datetime.timedelta(weeks=1)
		self.assertEquals(project.status(),'Finished')