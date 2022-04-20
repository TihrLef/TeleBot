class StatusTest(TestCase):
	def setUpTestData(cls):
		Project.objects.create_user(name='testProject')
	
	def test_in_progress(self):
		project=Project.objects.get(id=1)
		project.start_date=datetime.date.today()-datetime.timedelta(weeks=3)
		project.end_date=datetime.date.today()+datetime.timedelta(weeks=3)
		self.assertEquals(project.status,'in progress')
		
	def test_waiting(self):
		project=Project.objects.get(id=1)
		project.start_date=datetime.date.today()+datetime.timedelta(weeks=2)
		project.end_date=datetime.date.today()+datetime.timedelta(weeks=3)
		self.assertEquals(project.status,'waiting for start')
		
		
	def test_finished(self):
		project=Project.objects.get(id=1)
		project.start_date=datetime.date.today()-datetime.timedelta(weeks=3)
		project.end_date=datetime.date.today()-datetime.timedelta(weeks=1)
		self.assertEquals(project.status,'finished')