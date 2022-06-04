from django.urls import re_path
import django
import Projects.views
from . import views
from Projects.models import Project
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.views.static import serve
from web import settings




urlpatterns = [
	re_path(r'^project/(?P<pk>\d+)/change/$', Projects.views.project_change, name = "project-change"),
	re_path(r'projects', Projects.views.project_list, name='projects'),
	re_path(r'^project/(?P<pk>\d+)$',(Projects.views.ProjectDetailView.as_view()), name='project-detail'),
	re_path(r'project/create',  Projects.views.project_add, name = "project-create")
	
	]
