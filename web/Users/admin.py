from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import UserCreationForm, UserChangeForm
from .models import User

class UserAdmin(admin.ModelAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    add_fieldsets = (
        (None, {"fields": ("username", 
                           "password", 
                           "password2", 
                           "telegram_id")}),)
    list_display = ["username", "telegram_id"]

admin.site.register(User, UserAdmin)