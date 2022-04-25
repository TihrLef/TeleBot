from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .forms import MyUserCreationForm
from .forms import MyUserCreationFormreg

class SignUpView(CreateView):
    form_class = MyUserCreationFormreg
    success_url = reverse_lazy("login")
    #template_name = "registration/signup.html"
    template_name = "registration/signup_reg.html"
class SignUpView1(CreateView):
    form_class = MyUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
    
