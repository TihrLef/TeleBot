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
from django.forms import ModelForm
from django.http import HttpResponseRedirect
from django.urls import reverse
import tempfile
from tempfile import TemporaryDirectory as td

from threading import Thread
import time

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
	
class UsersListView(generic.ListView):
	model = User

@user_passes_test(User.is_verified)
def sort_index(request):
	project_list = Project.objects.order_by("name")
	return render(
		request,
		'Projects/project_list.html',
		context = {'project_list': project_list})


class ProjectsListView(generic.ListView):
	model = Project


@user_passes_test(User.is_verified)
def report(request):
	users = User.objects.all()
	projects = Project.objects.all()
	reports = Report.objects.all()
	error_message = ''
	
	if request.method == 'POST':
		data = FilterForm(request.POST)
		if(data.is_valid()):
			data = data.cleaned_data
			print(data)
			FaceControl = lambda rep: (not data['project'] or str(rep.project) in [str(project.name) for project in data['project']]) and\
									(not data['user'] or str(rep.user) in [str(user.username) for user in data['user']]) and\
									(not data['left_date'] or data['left_date'] <= rep.report_date) and\
									(not data['right_date'] or rep.report_date<= data['right_date']) and\
									(str(request.user) == str(rep.user) or request.user.is_staff or\
									str(request.user) == str(rep.project.responsible_user))
			reports = list(filter(FaceControl, reports))
		else:
			error_message = 'incorrect input data'
			reports = None

	form = FilterForm(request.POST) if request.method == 'POST' else FilterForm
	context = {'reports': reports,
			 'projects': projects,
			 'users': users,
			 'error_message': error_message,
			 'form': form}

	if reports:
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
		pdf.output(r"TeleBot/static/TempPdf/simple_demo.pdf", "F")
	return render(
		request,
		'Reports/reports_list.html',
		context = context)


@user_passes_test(User.is_verified)
def make_pdf(request):
	webbrowser.open_new(r"TeleBot/static/TempPdf/simple_demo.pdf")
	return redirect('reports')

class ProjectDetailView(generic.DetailView):
	model = Project

@user_passes_test(User.is_verified)	
def project_detail(request,pk):
	try:
		project=Project.objects.get(pk=pk)
	except Project.DoesNotExist:
		raise Http404("Такого проекта не существует!")
	if request.user.is_staff or request.user == project.responsible_user:
		reports = project.report_set.all()
	else:
		reports = project.report_set.all().filter(user=request.user)
	return render(
		request,
		'Projects/project_detail.html',
		context={'project':project, 'reports':reports}
	)

	
class ProjectModelForm(ModelForm):
	class Meta:
		model = Project
		fields = '__all__'

@user_passes_test(User.is_verified)	
def project_add(request):
	# Если данный запрос типа POST, тогда
	if request.method == 'POST':
		# Создаём экземпляр формы и заполняем данными из запроса (связывание, binding):
		form = ProjectModelForm(request.POST)
		# Проверка валидности данных формы:
		if form.is_valid():
			# Обработка данных из form.cleaned_data
			project = Project.objects.create(name = form.cleaned_data['name'])
			for user in form.cleaned_data['users']:
				project.users.add(user)
			project.responsible_user = form.cleaned_data['responsible_user']
			if project.responsible_user not in form.cleaned_data['users']:
				project.users.add(project.responsible_user)
			project.start_date = form.cleaned_data['start_date']
			project.end_date = form.cleaned_data['end_date']
			project.save()
			return HttpResponseRedirect(reverse('project-detail', args=[project.pk]))
	# Если это GET (или какой-либо ещё), создать форму по умолчанию.
	else:
		form = ProjectModelForm()
	return render(request, 'Projects/project_form.html', {'form': form})

@user_passes_test(User.is_verified)	
def project_change(request, pk):
	try:
		project=Project.objects.get(pk=pk)
	except Project.DoesNotExist:
		raise Http404("Такого персонажа не существует!")
	# Если данный запрос типа POST, тогда
	if request.method == 'POST':
		# Создаём экземпляр формы и заполняем данными из запроса (связывание, binding):
		form = ProjectModelForm(request.POST)
		# Проверка валидности данных формы:
		if form.is_valid():
			project.name = form.cleaned_data['name']
			for user in form.cleaned_data['users']:
				project.users.add(user)
			project.responsible_user = form.cleaned_data['responsible_user']
			if project.responsible_user not in form.cleaned_data['users']:
				project.users.add(project.responsible_user)
			project.start_date = form.cleaned_data['start_date']
			project.end_date = form.cleaned_data['end_date']
			project.save()
			return HttpResponseRedirect(reverse('project-detail', args=[project.pk]))
	# Если это GET (или какой-либо ещё), создать форму по умолчанию.
	else:
		form = ProjectModelForm(instance=project)
	return render(request, 'Projects/project_form.html', {'form': form})

class UserDetailView(generic.DetailView):
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

def token_valid(request):
	pass

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

'''

def person_detail_view(request,pk):
	try:
		person_id=Person.objects.get(id=pk)
	except Project.DoesNotExist:
		raise Http404("Такого персонажа не существует!")

	return render(
		request,
		'person/person_detail.html',
		context={'person':person_id,}
	)
'''