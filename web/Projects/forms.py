from django import forms
from django.forms import ModelForm
from .models import Project

class ProjectModelForm(ModelForm):
	class Meta:
		model = Project
		fields = '__all__'