from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from Projects import views
from Users.views import SignUpView
urlpatterns = []

urlpatterns += [
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("sign_up/", include("Users.urls")),
    path("admin/", admin.site.urls),
    path("sign_up/", include ("Users.urls"), name = "signup"),
    path("accounts/", include("django.contrib.auth.urls")),
    path('TeleBot/', include('TeleBot.urls')),
]