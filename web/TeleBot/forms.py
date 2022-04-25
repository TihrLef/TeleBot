from django import forms
from Projects.models import Project
from Users.models import User

class FilterForm(forms.Form):
    user = forms.ModelMultipleChoiceField(queryset = User.objects.all())
    project = forms.ModelMultipleChoiceField(queryset = Project.objects.all())
    left_date = forms.DateField(widget=forms.DateInput(attrs={'placeholder': 'mm/dd/yyyy'}))
    right_date = forms.DateField(widget=forms.DateInput(attrs={'placeholder': 'mm/dd/yyyy'}))
    