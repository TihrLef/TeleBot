from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UpdateUserForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from .forms import UserCreationForm
from .forms import UserCreationFormreg
from .forms import VerifiedToken
from .models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.urls import reverse
from web.settings import REF_TO_BOT
from django.http import Http404
from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test
from Users.models import User
from django.contrib.auth.mixins import AccessMixin
from Users.forms import UserModelForm
from django.contrib.admin.views.decorators import staff_member_required







class StaffMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
	
class OwnerOnlyMixin(AccessMixin):
    def handle_no_permission(self):
        return super().handle_no_permission()
    def dispatch(self, request, pk, *args, **kwargs):
        user_page = self.get_object()
        if request.user.telegram_id != user_page.telegram_id and not request.user.is_staff :
            return self.handle_no_permission()
        return super().dispatch(request, pk, *args, **kwargs)
	
#TODO миксины верхний удалить админскую часть



class SignUpView(CreateView):
    form_class = UserCreationFormreg
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
	return render(request, 'registration/signup_reg.html', context = {"form": VerifiedToken(), "ermsg": error_message, "REF_TO_BOT": REF_TO_BOT})    
   
def user_change(request, pk):
    try:
        user=User.objects.get(pk=pk)
    except User.DoesNotExist:
        error_message = "user deleted"
    if (request.method =='POST'):
        form = UserCreationForm(request.POST, instance=user)
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
        form = UserCreationForm(instance=user)
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


class UsersListView(StaffMixin, generic.ListView):
	model = User
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['user_list'] = User.objects.exclude(role = "Archived")
		return context

	
class ArchivedUsersListView(StaffMixin, generic.ListView):
	model = User
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['user_list'] = User.objects.filter(role = "Archived")
		return context

class UserDetailView(OwnerOnlyMixin, generic.DetailView):
	model = User

@staff_member_required
def archive_user(request, pk):
	user = User.objects.get(pk = pk)
	if user.is_active:
		user.is_active = False
		user.role = "Archived"
	else:
		user.is_active = True
		if user.is_staff:
			user.role = "Administrator"
		else:
			if user.last_login is None:
				user.role = "Unverified"
			else:	
				user.role = "Verified"
	user.save()
	return redirect(reverse('user-detail', args=[pk]))

@staff_member_required
def user_role_change(request, pk):
    user = User.objects.get(pk = pk)
    if request.method == "POST":
        user.role = request.POST['role']
        if user.role == "Administrator":
            user.is_staff=True
            user.is_active=True
        if user.role == "Verified":
            user.is_staff=False
            user.is_active=True
        if user.role == "Unverified":
            user.is_staff=False
            user.is_active=False
        #form = UserModelForm(request.POST)
        #if(form.is_valid()):
            #user.role = form.cleaned_data['role']
        user.save()
    return HttpResponseRedirect(reverse('user-detail', args=[user.pk]))

#Вывод списка пользователей с возможностью для админов верификации новых пользователей
@staff_member_required
def user_list(request):
	user_list = User.objects.exclude(role = "Archived")
	if request.method == "POST":
		id_list = request.POST.getlist('boxes')
		if request.POST['action'] == "Удалить":
			for user_id in id_list:
				try:
					User.objects.filter(pk=int(user_id)).delete()
				except User.DoesNotExist:
					pass
		else:
			for user_id in id_list:
				try:
					User.objects.filter(pk=int(user_id)).update(is_active=True)
					User.objects.filter(pk=int(user_id)).update(role = "Verified")
				except User.DoesNotExist:
					pass
	return render(request, 'Users/user_list.html', {"user_list" : user_list})


