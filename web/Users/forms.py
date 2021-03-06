from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User
from .models import Post
from django.forms import ModelForm
from django.contrib.admindocs.utils import ROLES


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

class UserModelForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('role',)
        #widgets = {'role' : forms.MultipleChoiceField(choices=Post.role_choices)}
    #class Meta:
        #model = Post
        #role = forms.ChoiceField(choices=choices, widget=forms.RadioSelect())
        #fields = tuple(["role",])
            #choices = (('Verified', 'Verified'), ('Unverified', 'Unverified'), ('Administrator', 'Administrator'),)
            #role = forms.ModelChoiceField(queryset = choices.all(), widget=forms.RadioSelect())
        #widgets = {'role': forms.RadioSelect(attrs={'name': 'role'}, choices=choices)}
       
class UpdateUserForm(UserChangeForm):
    class Meta:
        model = User
        fields = tuple(["username", "first_name", "last_name"])

class UserCreationFormreg(UserCreationForm):
    class Meta:
        model = User
        fields = ("telegram_id",)