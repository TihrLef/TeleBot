from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Project, User

def index(request):
	return render(
		request,
		'index.html',
		context={},
	)
	

class ProjectsListView(generic.ListView):
	model = Project
	
class ProjectDetailView(generic.DetailView):
	model = Project

class UsersListView(generic.ListView):
	model = User
	
class UsersDetailView(generic.DetailView):
	model = User
	
	
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