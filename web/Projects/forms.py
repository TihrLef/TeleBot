from django import forms
from django.core.exceptions import ValidationError

class ChangeProjectForm(forms.Form):
    name = forms.DateField()
	start_date = forms.DateField(help_text="Enter a date between now and 4 weeks (default 3).")
	#end_date
	#users
	#responsible_user
	
    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        #Проверка того, что дата не выходит за "нижнюю" границу (не в прошлом).
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))

        #Проверка того, то дата не выходит за "верхнюю" границу (+4 недели).
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

        # Помните, что всегда надо возвращать "очищенные" данные.
        return data