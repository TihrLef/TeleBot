from django.urls import path
from django.urls import re_path
from . import views
from .views import SignUpView
from .views import profile_edit, ChangePasswordView


urlpatterns =[
	path("sign_up/", SignUpView.as_view(), name="signup"),
	path("success", views.home, name="home"),
]