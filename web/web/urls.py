from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from django.views.generic import RedirectView
from Users import views
from Users.models import User
import Users.views 
from Users.views import VerifiedTokenFunction
from Users.views import SignUpView, ChangePasswordView, profile_edit
from Users.views import user_change
from django.urls import re_path


urlpatterns = []

urlpatterns += [
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("admin/", admin.site.urls, name="admin"),
    path("accounts/", include("django.contrib.auth.urls")),
    path('TeleBot/', include('TeleBot.urls')),
    path("password_change/", ChangePasswordView.as_view(), name='password_change'),
    path("edit/", views.profile_edit, name="edit"),
    path("signup/", VerifiedTokenFunction, name="signup"),
    path("success", views.home, name="home"),
    path('User/', include('Users.urls')),
]
urlpatterns += [re_path("signup_reg/(?P<pk>\d+)$", user_change, name="signup_reg"),]
urlpatterns += [path("adminka", RedirectView.as_view(url='/admin', permanent=True), name="adminka"),]
