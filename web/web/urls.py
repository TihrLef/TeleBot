from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from django.views.generic import RedirectView
import Users
from Users import urls
from Users.views import VerifiedTokenFunction
from Users.views import SignUpView, ChangePasswordView, profile_edit
from Users.views import user_change
from django.urls import re_path
from django.views.static import serve
from . import settings
from . import views


urlpatterns = []

urlpatterns += [
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("admin/", admin.site.urls, name="admin"),
    path("accounts/", include("django.contrib.auth.urls")),
	path("", include('Reports.urls')),
	path("success",  (TemplateView.as_view(template_name="success.html")), name="success"),
	path('contact-page/', views.contact_page, name = "contact-page"), 
	path('contact-page/send-contact/', views.send_contact, name = "send-contact"), 
	path("", include('Projects.urls')),
	path("", include('Users.urls')),
    path("password_change/", Users.views.ChangePasswordView.as_view(), name='password_change'),
    path("edit/", Users.views.profile_edit, name="edit"),
    path("signup/", VerifiedTokenFunction, name="signup"),
    path("success", Users.views.home, name="home"),
]
urlpatterns += [re_path("signup_reg/(?P<pk>\d+)$", user_change, name="signup_reg"),]
urlpatterns += [path("adminka", RedirectView.as_view(url='/admin', permanent=True), name="adminka"),]
