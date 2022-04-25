from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User



class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "telegram_id", "first_name", "last_name")

class MyUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = tuple(["username"])
class MyUserCreationFormreg(UserCreationForm):
    class Meta:
        model = User
        fields = ("telegram_id",)