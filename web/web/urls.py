"""custom_user URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from Projects import views
urlpatterns = []

urlpatterns += [
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("admin/", admin.site.urls),
    path("accounts/", include("Users.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
]

urlpatterns += [path('TeleBot/', include('TeleBot.urls')),]
'''
urlpatterns += [
    re_path(r'^$', views.index, name='index'),
	re_path(r'^projects/$', views.ProjectsListView.as_view(), name='projects'),
	re_path(r'^project/(?P<pk>\d+)$', views.ProjectDetailView.as_view(), name='project-detail'),
	re_path(r'^users/$', views.UsersListView.as_view(), name='users'),
	#re_path(r'^person/(?P<pk>\d+)$', views.PersonDetailView.as_view(), name='person-detail'),
]'''