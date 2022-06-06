from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse
from django.contrib.auth.mixins import AccessMixin
from Projects.models import Project
from Users.models import User
from .forms import ProjectModelForm
from django.views import generic
from django.http import Http404

class ProjectAccessMixin(AccessMixin):
    def handle_no_permission(self):
        return super().handle_no_permission()
    def dispatch(self, request, pk, *args, **kwargs):
        project_page = self.get_object()
        if (project_page not in request.user.project_set.all()) and not request.user.is_staff :
            return self.handle_no_permission()
        return super().dispatch(request, pk, *args, **kwargs)



@user_passes_test(User.is_verified)
def project_list(request):
	project_list = Project.objects.order_by("end_date", "start_date")
	return render(
		request,
		'Projects/project_list.html',
		context = {'project_list': project_list})
		
class ProjectDetailView(ProjectAccessMixin, generic.DetailView):
	model = Project

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		if self.request.user.is_staff or self.request.user == context['project'].responsible_user:
			reports = context['project'].report_set.all()
		else:
			reports = context['project'].report_set.all().filter(user=self.request.user)
		context['reports'] = reports
		return context

@user_passes_test(User.is_verified)	
def project_detail(request,pk):
	try:
		project=Project.objects.get(pk=pk)
	except Project.DoesNotExist:
		raise Http404("Такого проекта не существует!")
	if request.user.is_staff or request.user in project.users.all():
		if request.user.is_staff or request.user == project.responsible_user:
			reports = project.report_set.all()
		else:
			reports = project.report_set.all().filter(user=request.user) 
		return render(
			request,
			'Projects/project_detail.html',
			context={'project':project, 'reports':reports}
		)
	else:
		return HttpResponseRedirect(reverse('projects'))

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
	return render(request, 'Projects/project_form.html', context = {'available_users': User.objects.all().filter(is_active=True), 'form': form})
	
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
		return HttpResponseRedirect(reverse('projects'))
	return render(request, 'Projects/project_form.html', context = {'available_users': User.objects.all().filter(is_active=True), 'selected_users': project.users.all(), 'form': form})