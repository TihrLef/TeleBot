from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from Projects.models import Project
from Users.models import User
from Reports.models import Report
from fpdf import FPDF

# Ответ на вызов основного сайта
# Адрес: /TeleBot
def index(request):
	return render(
		request,
		'index.html',
		context={},
	)
	
class UsersListView(generic.ListView):
	model = User


def sort_index(request):
	project_list = Project.objects.order_by("name")
	return render(
		request,
		'Projects/project_list.html',
		context = {'project_list': project_list})

class ProjectsListView(generic.ListView):
	model = Project

def report(request):
	reports = Report.objects.all()
	return render(
		request,
		'Reports/reports_list.html',
		context = {'reports': reports})

def make_pdf(request):
	return render(
		request,
		"help.html")

class ProjectDetailView(generic.DetailView):
	model = Project
	
def project_detail_view(request,pk):
	try:
		project_id=Project.objects.get(pk=pk)
	except Project.DoesNotExist:
		raise Http404("Такого проекта не существует!")

	return render(
		request,
		'project/project_detail.html',
		context={'project':project_id,}
	)
	
class UserDetailView(generic.DetailView):
	model = User
	
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