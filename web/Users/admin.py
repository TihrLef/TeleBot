from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import MyUserCreationForm, MyUserChangeForm
from .models import User

class MyUserAdmin(admin.ModelAdmin):
    add_form = MyUserCreationForm
    form = MyUserChangeForm
    model = User
    fields = ['username', 'password',  'telegram_id']
    list_display = ["username","email", "telegram_id"]

admin.site.register(User, MyUserAdmin)