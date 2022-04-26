from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import MyUserCreationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import MyUpdateUserForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from .forms import MyUserCreationForm
from .forms import MyUserCreationFormreg
from .forms import VerifiedToken
from .models import User
from _ast import Try
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.urls import reverse


class SignUpView(CreateView):
    form_class = MyUserCreationFormreg
    success_url = reverse_lazy("login")
    #template_name = "registration/signup.html"
    template_name = "registration/signup.html"

def VerifiedTokenFunction(request):
	error_message = ''
	token = None
	if request.method == 'POST':
		token = request.POST['personal_token']
		try:
			user = User.objects.get(personal_token=token)
			if user.first_name:
				error_message = "Вы уже зарегистрированы в системе!"
			else:
				return HttpResponseRedirect(reverse('signup_reg', args=[user.pk]))
		except ValidationError:
			error_message = "Введённое вами <i>нечто</i> токеном не является!"
		except User.DoesNotExist:
			error_message = "Пользователя с таким токеном не существует"
	return render(request, 'registration/signup_reg.html', context = {"form": VerifiedToken(), "ermsg": error_message})    
   
def user_change(request, pk):
    try:
        user=User.objects.get(pk=pk)
    except User.DoesNotExist:
        error_message = "user deleted"
    if (request.method =='POST'):
        form = MyUserCreationForm(request.POST)
        # Проверка валидности данных формы:
        if form.is_valid():
            user.username = form.cleaned_data['username']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.set_password(form.cleaned_data['password1'])
            user.save()
            return HttpResponseRedirect(reverse('login'))
    # Если это GET (или какой-либо ещё), создать форму по умолчанию.
    else:
        form = MyUserCreationForm(instance=user)
    return render(request, 'registration/signup.html', {'form': form})  
  
class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('success')

@login_required
def home(request):
    tel_id = request.user.telegram_id
    return HttpResponseRedirect(f'Telebot/user/{tel_id}/')

@login_required
def profile_edit(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='/TeleBot/success')
    else:
        user_form = UpdateUserForm(instance=request.user)

    return render(request, "edit.html", {'user_form': user_form})

