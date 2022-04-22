from django.urls import path
from django.urls import re_path
from . import views
from Projects.models import Project
from Users.models import User
from Reports.models import Report

#Не трогайте эту строчку! Добавляйте новые ниже!
urlpatterns = []

urlpatterns += [
    re_path(r'^$', views.index, name='index'),
	re_path(r'^projects/$', views.ProjectsListView.as_view(), name='projects'),
	re_path(r'^project/(?P<pk>\d+)$', views.ProjectDetailView.as_view(), name='project-detail'),
	re_path(r'^users/$', views.UsersListView.as_view(), name='users'),
	re_path(r'^user/(?P<pk>\d+)$', views.UserDetailView.as_view(), name='user-detail'),
	#re_path(r'^reports/my)$', views.ReportsListView.as_view(), name='user-detail'),
	#re_path(r'^reports/$', views.UsersListView.as_view(), name='users'),
]