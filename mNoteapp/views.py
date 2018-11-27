from django.views import generic
from django.views.generic.edit import CreateView
from .forms import *
from django.urls import reverse_lazy

class SignUp(CreateView):
    form_class = AppUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
