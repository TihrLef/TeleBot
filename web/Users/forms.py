from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name")
'''
class VerifiedToken(forms.Form):
    personal_token = forms.UUIDField( help_text="Unique ID for this particular book across whole library")
    telegram_id = forms.IntegerField()
'''

class MyUpdateUserForm(UserChangeForm):
    class Meta:
        model = User
        fields = tuple(["username"])
class MyUserCreationFormreg(UserCreationForm):
    class Meta:
        model = User
        fields = ("telegram_id",)