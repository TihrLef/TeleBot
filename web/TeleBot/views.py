from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test
from Projects.models import Project
from Users.models import User
from Reports.models import Report
from fpdf import FPDF
from django.http import Http404
from django.views.generic.edit import CreateView, UpdateView
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.urls import reverse
import tempfile
from tempfile import TemporaryDirectory as td
from django.contrib.auth.mixins import AccessMixin
from threading import Thread
import time
from Users.forms import UserModelForm
from django.contrib.admin.views.decorators import staff_member_required


from django.db.models import Q


import web.urls


# РћС‚РІРµС‚ РЅР° РІС‹Р·РѕРІ РѕСЃРЅРѕРІРЅРѕРіРѕ СЃР°Р№С‚Р°
# РђРґСЂРµСЃ: /TeleBot
@user_passes_test(User.is_verified)
def index(request):
	return render(
		request,
		'index.html',
		context={},
	)

