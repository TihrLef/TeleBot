from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from Projects.models import Project
from Users.models import User
from Reports.models import Report
from .forms import FilterForm
from fpdf import FPDF
import webbrowser

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
		pdf.add_font("Sans", style = "", fname = r"C:\Users\Георгий\Desktop\Work\Programming\Projects\Python\Работа в ЛЭТИ\TeleBot\web\TeleBot\static\Fonts\OpenSans\OpenSans-Regular.ttf", uni=True)
		pdf.add_font("Sans", style = "B", fname = r"C:\Users\Георгий\Desktop\Work\Programming\Projects\Python\Работа в ЛЭТИ\TeleBot\web\TeleBot\static\Fonts\OpenSans\OpenSans-Bold.ttf", uni=True)
		for report in reports:
			pdf.set_font("Sans", style = "B", size = 12)
			pdf.multi_cell(w = 200, h = 8, txt = 'Project name: ' + report.project.name, align = "L", ln = 1)
			pdf.multi_cell(w = 200, h = 8, txt = 'Week: ' + str(report.report_date), align = "L", ln = 1)
			pdf.multi_cell(w = 200, h = 8, txt = 'Last author: ' + report.user.username, align = "L", ln = 1)
			pdf.multi_cell(w = 200, h = 8, txt = 'Message:', align = "L", ln = 1)
			pdf.set_font("Sans", style = "", size = 12)
			pdf.multi_cell(w = 200, h = 8, txt = report.message, align = "L", ln = 1)
			pdf.multi_cell(w = 200, h = 10, txt = '\n', align = "L", ln = 1)
		pdf.output(r"TeleBot\static\TempPdf\simple_demo.pdf", "F")
	return render(
		request,
		'Reports/reports_list.html',
		context = context)

def make_pdf(request):
	webbrowser.open_new(r"TeleBot\static\TempPdf\simple_demo.pdf")
	return redirect('reports')

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