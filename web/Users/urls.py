from django.urls import path
from django.urls import re_path
from . import views
from .views import SignUpView
from .views import profile_edit, ChangePasswordView


urlpatterns =[
	path("edit/", views.profile_edit, name="edit"),
    path("password_change/", ChangePasswordView.as_view(), name='password_change'),
	path("sign_up/", SignUpView.as_view(), name="signup"),
	path("success", views.home, name="home"),
]