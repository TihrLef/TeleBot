from django.urls import re_path
import django
from . import views
from Reports.models import Report
from web import settings
from django.views.static import serve
from django.conf.urls.static import static


#Не трогайте эту строчку! Добавляйте новые ниже!
urlpatterns = []
urlpatterns += [re_path('static/(?P<path>.*)$', django.views.static.serve, {'document_root': settings.STATIC_ROOT, 'show_indexes': settings.DEBUG})]
urlpatterns += [re_path(r'^reports/$', views.report, name = "reports")]
urlpatterns += [re_path(r'^help/$', views.make_pdf, name = "maker_pdf")] 
