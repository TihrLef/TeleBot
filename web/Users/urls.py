from django.urls import path
from django.urls import re_path
from . import views
from .views import SignUpView
from .views import profile_edit, ChangePasswordView
from .views import VerifiedTokenFunction

urlpatterns = []
urlpatterns += [
    path("signup_reg/",SignUpView.as_view(), name="signup_reg"),
    path("signup/", VerifiedTokenFunction, name="signup"),
]