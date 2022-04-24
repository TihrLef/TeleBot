from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from Projects import views
from Users import views
import Users.views
from Users.views import SignUpView, ChangePasswordView, profile_edit
urlpatterns = []

urlpatterns += [
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("sign_up/", include("Users.urls")),
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path('TeleBot/', include('TeleBot.urls')),
    path("password_change/", ChangePasswordView.as_view(), name='password_change'),
	path("edit/", views.profile_edit, name="edit"),
]