from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test
from Users.models import User
from django.core.mail import send_mail
from django.urls import reverse


@user_passes_test(User.is_verified)
def index(request):
	return render(
		request,
		'index.html',
		context={},
	)

@user_passes_test(User.is_verified)
def send_contact(request):
     name = request.POST.get("name")
     email = request.POST.get("email")
     subject = request.POST.get("subject")
     message = request.POST.get("message")
     send_mail("Новое сообщение", message, email, ["telebotsupp@yandex.ru"],
    html_message="<html> Новое сообщение с сайта<br>"
      "Имя:" + name + '<br>'
      "Email почта:" + email + '<br>'
      "Тема:" + subject + '<br>'
       "Сообщение:" + message + "<br>"
   "</html>")
     request.session['sendmessage'] = "Сообщение было отправлено"
     return redirect(reverse('contact-page'))

def contact_page(request):
    return render(request, "contact.html")