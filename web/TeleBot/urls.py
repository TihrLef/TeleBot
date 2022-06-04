from django.urls import path
from django.urls import re_path
import django
import Projects.views
from . import views
from Projects.models import Project
from Users.models import User
from Reports.models import Report
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.views.static import serve
from web import settings


#Не трогайте эту строчку! Добавляйте новые ниже!
urlpatterns = []
#urlpatterns +=[re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),]

urlpatterns += [re_path("success",  user_passes_test(User.is_verified)(TemplateView.as_view(template_name="success.html")), name="success"),
				re_path("", views.index, name="index")]


#urlpatterns += [re_path(r'^requests/$', staff_member_required(views.admin_approval), name='unver_users')]
