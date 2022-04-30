from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test
from Projects.models import Project
from Users.models import User
from Reports.models import Report
from .forms import FilterForm
from fpdf import FPDF
from django.views.generic.edit import CreateView, UpdateView
from django.http import HttpResponseRedirect
from django.urls import reverse
import tempfile
from tempfile import TemporaryDirectory as td
from django.contrib.auth.mixins import AccessMixin
from threading import Thread
import time
from django.contrib.admin.views.decorators import staff_member_required

class OwnerOnlyMixin(AccessMixin):
    def handle_no_permission(self):
        return super().handle_no_permission()
    def dispatch(self, request, pk, *args, **kwargs):
        user_page = self.get_object()
        if request.user.telegram_id != user_page.telegram_id and not request.user.is_staff :
            return self.handle_no_permission()
        return super().dispatch(request, pk, *args, **kwargs)
	


import web.urls

class TempDir:
	def __init__(self):
		self.name = None
	def MakeDir(self, path = None, prefix = '', lifetime = 0):
		th = Thread(target = self.creation, args=(path, prefix, lifetime))
		th.start()
		while self.name is None:
			time.sleep(0.01)

	def creation(self, path = None, prefix = '', lifetime = 0):
		if path:
			tempfile.tempdir = path
		temp = td(prefix = prefix)
		self.name = str(temp.name)
		time.sleep(lifetime)

# Ответ на вызов основного сайта
# Адрес: /TeleBot
@user_passes_test(User.is_verified)
def index(request):
	return render(
		request,
		'index.html',
		context={},
	)

def available_reports(request):
	return list(filter(lambda rep: (str(request.user) == str(rep.user) or request.user.is_staff or\
									str(request.user) == str(rep.project.responsible_user)), 
					   Report.objects.order_by("project")))

def available_projects(request):
	if request.user.is_staff:
		return list(Project.objects.all())
	return list(request.user.project_set.all())

def available_users(request):
	if request.user.is_staff:
		return list(User.objects.all())
	users = []
	for project in available_projects(request):
			if(str(request.user) == str(project.responsible_user)):
				users += [user for user in project.users.all()]
	return list(set(users))

def make_pdf(request, reports, path):
	temp = TempDir()
	temp.MakeDir(path = path, prefix = 'TempPdf', lifetime = 180)
	name = temp.name
	pdf = FPDF()
	pdf.add_page()
	pdf.add_font("Sans", style = "", fname = r"TeleBot/static/Fonts/OpenSans/OpenSans-Regular.ttf", uni=True)
	pdf.add_font("Sans", style = "B", fname = r"TeleBot/static/Fonts/OpenSans/OpenSans-Bold.ttf", uni=True)
	for report in reports:
		pdf.set_font("Sans", style = "B", size = 12)
		pdf.multi_cell(w = 200, h = 8, txt = 'Project name: ' + report.project.name, align = "L", ln = 1)
		pdf.multi_cell(w = 200, h = 8, txt = 'Week: ' + str(report.report_date), align = "L", ln = 1)
		pdf.multi_cell(w = 200, h = 8, txt = 'Last author: ' + report.user.username, align = "L", ln = 1)
		pdf.multi_cell(w = 200, h = 8, txt = 'Message:', align = "L", ln = 1)
		pdf.set_font("Sans", style = "", size = 12)
		pdf.multi_cell(w = 200, h = 8, txt = report.message, align = "L", ln = 1)
		pdf.multi_cell(w = 200, h = 10, txt = '\n', align = "L", ln = 1)
	pdf.output(name + r"/simple_demo" + str(request.user) + ".pdf", "F")
	return name

@user_passes_test(User.is_verified)
def report(request):
	reports = available_reports(request)
	error_message = ''
	
	if request.method == 'POST':
		data = FilterForm(request.POST)
		if(data.is_valid()):
			data = data.cleaned_data
			print(data)
			FaceControl = lambda rep: (not data['project'] or str(rep.project) in [str(project.name) for project in data['project']]) and\
									  (not data['user'] or str(rep.user) in [str(user.username) for user in data['user']]) and\
									  (not data['left_date'] or data['left_date'] <= rep.report_date) and\
									  (not data['right_date'] or rep.report_date <= data['right_date'])
			reports = list(filter(FaceControl, reports))
		else:
			error_message = 'incorrect input data'
			reports = []

	path = r"TeleBot/static"
	name = make_pdf(request, reports, path)
	
	projects = available_projects(request)
	users = available_users(request)
	if len(users) == 1:
		users.clear()
	if len(projects) == 1:
		projects.clear()
	return render(
		request,
		'Reports/reports_list.html',
		context = {'reports': reports,
			 'projects': projects,
			 'available_users': users,
			 'error_message': error_message,
			 'form': FilterForm(request.POST) if request.method == 'POST' else FilterForm(),
			 'pdfname': name[len(path):] + r"/simple_demo" + str(request.user) + ".pdf"})
	

class UsersListView(generic.ListView):
	model = User

class UserDetailView(OwnerOnlyMixin, generic.DetailView):
	model = User

@user_passes_test(User.is_verified)	
def user_detail(request,pk):
	try:
		tele_id=User.objects.get(telegram_id=pk)
	except User.DoesNotExist:
		raise Http404("Такого персонажа не существует!")
	
	return render(
		request,
		'user/user_detail.html',
		context={'user':tele_id,}
	)

@staff_member_required
def user_list(request):
	user_list = User.objects.all
	if request.method == "POST":
		id_list = request.POST.getlist('boxes')
		if request.POST['action'] == "Удалить":
			for user_id in id_list:
				try:
					User.objects.filter(pk=int(user_id)).delete()
				except User.DoesNotExist:
					pass
		else:
			for user_id in id_list:
				try:
					User.objects.filter(pk=int(user_id)).update(is_active=True)
				except User.DoesNotExist:
					pass
	return render(request, 'Users/user_list.html', {"user_list" : user_list})
