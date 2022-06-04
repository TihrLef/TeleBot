from django.urls import path
from django.urls import re_path
from Users import views
from django.contrib.auth.decorators import user_passes_test


urlpatterns = [
	re_path(r'users/', views.user_list, name='users'),
	re_path(r'^users/archive$', views.ArchivedUsersListView.as_view(), name='archive'),
	re_path(r'^user/(?P<pk>\d+)$',  views.UserDetailView.as_view(), name='user-detail'),
	re_path(r'^user/(?P<pk>\d+)/archive-user$', views.archive_user, name='archive-user'),
	re_path(r'^user/(?P<pk>\d+)/role-user-change$', views.user_role_change, name='role-user-change'),
	]

