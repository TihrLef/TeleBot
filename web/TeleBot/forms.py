from django import forms
from Projects.models import Project
from Users.models import User

class FilterForm(forms.Form):
    user = forms.ModelMultipleChoiceField(queryset = User.objects.all(), required = False)
    project = forms.ModelMultipleChoiceField(queryset = Project.objects.all(), required = False)
    left_date = forms.DateField(widget=forms.DateInput(attrs={'placeholder': 'mm/dd/yyyy'}), required = False)
    right_date = forms.DateField(widget=forms.DateInput(attrs={'placeholder': 'mm/dd/yyyy'}), required = False)
    