from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User


class UserCreationForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name")
    ''' 
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise.forms.ValidationError()
        '''

class VerifiedToken(forms.Form):
    personal_token = forms.UUIDField( help_text="Unique ID for this particular book across whole library")
    #telegram_id = forms.IntegerField()


class UpdateUserForm(UserChangeForm):
    class Meta:
        model = User
        fields = tuple(["username", "first_name", "last_name"])
class UserCreationFormreg(UserCreationForm):
    class Meta:
        model = User
        fields = ("telegram_id",)