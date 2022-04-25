from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from Projects.models import Project
from Users.models import User
from Reports.models import Report

def index(request):
	return render(
		request,
		'index.html',
		context={},
	)
	
	
def sort_index(request):
	project_list = Project.objects.order_by("name")
	return render(
		request,
		'Projects/project_list.html',
		context = {'project_list': project_list})

class ProjectsListView(generic.ListView):
	model = Project

def report(request):
	return render(
		request,
		'Reports/reports_list.html',
		context = {'reports': Report.objects.all()})

class ProjectDetailView(generic.DetailView):
	model = Project
	
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

def project_add(request):
	return render(
		request,
		'Projects/project_add.html')
	
def project_change(request,pk):
	try:
		project=Project.objects.get(pk=pk)
	except Project.DoesNotExist:
		raise Http404("Такого проекта не существует!")

	return render(
		request,
		'Projects/project_change.html',
		context={'project':project}
	)

class UsersListView(generic.ListView):
	model = User
	
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
def token_valid(request):
	pass


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