from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import user_passes_test
from Projects.models import Project
from Users.models import User
from Reports.models import Report
from .forms import FilterForm
from fpdf import FPDF
import webbrowser
from django.views.generic.edit import CreateView, UpdateView

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
	print()
	print(str(projects[0].responsible_user) == str(projects[0].responsible_user))
	print()
	if request.method == 'POST':
		data = FilterForm(request.POST)
		if(data.is_valid()):
			print(request.user)
			data = data.cleaned_data
			print(data)
			FaceControl = lambda rep: str(rep.project) in [str(project.name) for project in data['project']] and\
									str(rep.user) in [str(user.username) for user in data['user']] and\
									data['left_date'] <= rep.report_date <= data['right_date'] and\
									(str(request.user) == str(rep.user) or\
									str(request.user) == str(rep.project.responsible_user))
			reports = list(filter(FaceControl, reports))
		else:
			error_message = 'incorrect input data'
			reports = None
	form = FilterForm()
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

class ProjectCreate(CreateView):
	model = Project
	fields = '__all__'

class ProjectUpdate(UpdateView):
	model = Project
	fields = '__all__'


@user_passes_test(User.is_verified)
def project_add(request):
	return render(
		request,
		'Projects/project_add.html')

@user_passes_test(User.is_verified)	
def project_change(request,pk):
	try:
		project=Project.objects.get(pk=pk)
	except Project.DoesNotExist:
		raise Http404("Такого проекта не существует!")
	users=Project.objects.all
	return render(
		request,
		'Projects/project_change.html',
		context={'project':project, 'users': users}
	)

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