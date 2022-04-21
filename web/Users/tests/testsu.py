from django.test import TestCase

from Users.models import User
class SUTest(TestCase)
	def testsu(self):
		us = User(username = "NeValera", password = "Berlingo", is_staff = True, telegram_id = 123456789, is_superuser = True)