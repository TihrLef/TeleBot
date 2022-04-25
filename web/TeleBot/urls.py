from django.urls import path
from django.urls import re_path
from . import views
from Projects.models import Project
from Users.models import User
from Reports.models import Report
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required



#Не трогайте эту строчку! Добавляйте новые ниже!
urlpatterns = []

urlpatterns += [
    re_path(r'^$', views.index, name='index'),
	re_path(r'^users/$', user_passes_test(User.is_verified)(views.UsersListView.as_view()), name='users'),
	re_path(r'^projects/$', views.sort_index, name='projects'),
	re_path(r'^project/(?P<pk>\d+)$', views.project_detail, name='project-detail'),
	re_path("success",  user_passes_test(User.is_verified)(TemplateView.as_view(template_name="success.html")), name="success"),
	]
urlpatterns += [re_path(r'^user/(?P<pk>\d+)$',  user_passes_test(User.is_verified)(views.UserDetailView.as_view()), name='user-detail') ]
urlpatterns += [re_path(r'^reports/$', views.report, name = "reports")]
urlpatterns += [re_path(r'^help/$', views.make_pdf, name = "maker_pdf")]
urlpatterns += [re_path(r'^projects/create$',  views.project_add, name = "project-create")]
urlpatterns += [re_path(r'^project/(?P<pk>\d+)/change/$', views.project_change, name = "project-change")]

#urlpatterns += [re_path(r'^project/(?P<pk>\d+)/changed/$', views.project_changed, name = "project-changed")]

#urlpatterns += [re_path(r'^help/(&P<id>\d+)$', views.make_tests, name = "maker")]
