from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse

from TeleBot import urls
from Projects.models import Project
from Users.models import User
from .forms import ProjectModelForm


@user_passes_test(User.is_verified)
def project_list(request):
	project_list = Project.objects.order_by("end_date", "start_date")
	return render(
		request,
		'Projects/project_list.html',
		context = {'project_list': project_list})
		
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
	
@staff_member_required
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
	if request.user.is_staff or request.user == project.responsible_user:
		if request.method == 'POST':
			# Создаём экземпляр формы и заполняем данными из запроса (связывание, binding):
			form = ProjectModelForm(request.POST, instance=project)
			# Проверка валидности данных формы:
			if form.is_valid():
				print("i am here")
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
			print("Ya ne tam")
		# Если это GET (или какой-либо ещё), создать форму по умолчанию.
		else:
			form = ProjectModelForm(instance=project)
	else:
		HttpResponseRedirect(reverse('projects'))
	return render(request, 'Projects/project_form.html', {'form': form})