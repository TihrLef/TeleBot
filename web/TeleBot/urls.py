from django.urls import path
from django.urls import re_path
from . import views
from Projects.models import Project
from Users.models import User
from Reports.models import Report
from django.views.generic.base import TemplateView


#Не трогайте эту строчку! Добавляйте новые ниже!
urlpatterns = []

urlpatterns += [
    re_path(r'^$', views.index, name='index'),
	re_path(r'^users/$', views.UsersListView.as_view(), name='users'),
	re_path(r'^projects/$', views.sort_index, name='projects'),
	re_path(r'^project/(?P<pk>\d+)$', views.project_detail, name='project-detail'),
	re_path(r'^users/$', views.UsersListView.as_view(), name='users'),
	re_path("success", TemplateView.as_view(template_name="success.html"), name="success"),
]
urlpatterns += [re_path(r'^user/(?P<pk>\d+)$', views.UserDetailView.as_view(), name='user-detail') ]
urlpatterns += [re_path(r'^reports/$', views.report, name = "reports")]
urlpatterns += [re_path(r'^help/$', views.make_pdf, name = "maker_pdf")]
urlpatterns += [re_path(r'^projects/create$', views.ProjectCreate.as_view(), name = "project-create")]
urlpatterns += [re_path(r'^project/(?P<pk>\d+)/change/$', views.ProjectUpdate.as_view(), name = "project-change")]
#urlpatterns += [re_path(r'^project/(?P<pk>\d+)/changed/$', views.project_changed, name = "project-changed")]

#urlpatterns += [re_path(r'^help/(&P<id>\d+)$', views.make_tests, name = "maker")]
