from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import UserCreationForm, UserChangeForm
from .models import User




class UserAdmin(admin.ModelAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    fieldsets = (
       (None, {'fields': ('username', 'password','telegram_id')}),
       ('Personal info', {'fields': ('first_name', 'last_name')}),
		       ('Permissions', {'fields': ('is_active', 'is_staff')}),)
    add_fieldsets = (
        (None, {"fields": ( 'username','first_name','last_name','telegram_id',
						    'password1', 'password2'),}),)
    list_display = ["username", "telegram_id", "first_name", "last_name","is_verified", "personal_token"]

admin.site.register(User, UserAdmin)

