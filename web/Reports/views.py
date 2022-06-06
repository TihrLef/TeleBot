import os
from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth.decorators import user_passes_test
from Projects.models import Project
from Users.models import User
from Reports.models import Report
from .forms import FilterForm
from fpdf import FPDF
import tempfile
from tempfile import TemporaryDirectory as td
from threading import Thread
import time
from django.db.models import Q
from web import settings

def available_reports(request):
	if(request.user.is_staff):
		return Report.objects.all()
	return Report.objects.filter(Q(user__exact = request.user.telegram_id) |
							  Q(project__responsible_user__telegram_id__exact = request.user.telegram_id)).order_by('project')

def available_projects(request):
	if request.user.is_staff:
		return Project.objects.all()
	return request.user.project_set.all()

def available_users(request):
	if request.user.is_staff:
		return User.objects.all()
	users = User.objects.none()
	for project in available_projects(request):
			if(request.user.telegram_id == project.responsible_user.telegram_id):
				users = users | project.users.all()
	return users

def make_pdf(request, reports, path):
	os.makedirs(path, exist_ok = True)
	pdf = FPDF()
	pdf.add_page()
	pdf.add_font("Sans", style = "", fname = os.path.join(settings.BASE_DIR, "Reports/static/Fonts/OpenSans/OpenSans-Regular.ttf"), uni=True)
	pdf.add_font("Sans", style = "B", fname = os.path.join(settings.BASE_DIR, "Reports/static/Fonts/OpenSans/OpenSans-Bold.ttf"), uni=True)
	for report in reports:
		pdf.set_font("Sans", style = "B", size = 12)
		pdf.multi_cell(w = 200, h = 8, txt = 'Project name: ' + report.project.name, align = "L", ln = 1)
		pdf.multi_cell(w = 200, h = 8, txt = 'Week: ' + str(report.report_date), align = "L", ln = 1)
		pdf.multi_cell(w = 200, h = 8, txt = 'Last author: ' + report.user.username, align = "L", ln = 1)
		pdf.multi_cell(w = 200, h = 8, txt = 'Message:', align = "L", ln = 1)
		pdf.set_font("Sans", style = "", size = 12)
		pdf.multi_cell(w = 200, h = 8, txt = report.message, align = "L", ln = 1)
		pdf.multi_cell(w = 200, h = 10, txt = '\n', align = "L", ln = 1)
	pdf.output(path + r"/" + str(request.user) + ".pdf", "F")

@user_passes_test(User.is_verified)
def report(request):
	reports = available_reports(request)
	error_message = ''

	form = FilterForm()
	if request.method == 'POST':
		form = FilterForm(request.POST)
		if(form.is_valid()):
			data = form.cleaned_data
			if(data['project']):
				reports = reports.filter(project__id__in = data['project'])
			if(data['user']):
				reports = reports.filter(user__telegram_id__in = data['user'])
			if(data['left_date']):
				reports = reports.exclude(report_date__lte = data['left_date'])
			if(data['right_date']):
				reports = reports.filter(report_date__lte = data['right_date'])
		else:
			error_message = 'incorrect input data'
			reports = []

	path = r"Reports/static/pdf_folder"
	make_pdf(request, reports, path)

	projects = available_projects(request)
	users = available_users(request)
	if len(users) == 1:
		users.clear()
	if len(projects) == 1:
		projects.clear()
	print(form)
	return render(
		request,
		'Reports/reports_list.html',
		context = {'reports': reports,
			 'projects': projects,
			 'available_users': users,
			 'error_message': error_message,
			 'form': form,
			 'pdfname': r"pdf_folder/" + str(request.user) + ".pdf"})	