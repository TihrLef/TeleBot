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
#from .forms import VerifiedToken

class SignUpView(CreateView):
    form_class = MyUserCreationFormreg
    success_url = reverse_lazy("login")
    #template_name = "registration/signup.html"
    template_name = "registration/signup.html"
'''
def VerifiedTokenFunction(request):
    if request.method == 'POST':
        data = VerifiedToken(request.POST)
        if(data.is_valid()):
             data = data.cleaned_data
             
        print(data.cleaned_data)
    return render(request, 'registration/signup_reg.html', context = {"form": VerifiedToken()})       
'''
    

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

