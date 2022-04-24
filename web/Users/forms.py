from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User


class UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "is_superuser", "telegram_id", "is_staff", "first_name")

class UserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = tuple(["username"])
		
class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = User
        fields = ['username','first_name','last_name']
