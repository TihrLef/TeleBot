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
	re_path(r'^projects/$', views.sort_index, name='projects'),
	re_path(r'^project/(?P<pk>\d+)$', views.ProjectDetailView.as_view(), name='project-detail'),
	re_path(r'^users/$', views.UsersListView.as_view(), name='users'),
	#re_path(r'^person/(?P<pk>\d+)$', views.PersonDetailView.as_view(), name='person-detail'),
]