# -*- coding: utf-8 -*-

from django.urls import path

from .views import SignUpView
from .views import SignUpView1

urlpatterns = [
    path("signup_reg/",SignUpView.as_view(), name="signup_reg"),
    path("signup/", SignUpView1.as_view(), name="signup"),
    
]