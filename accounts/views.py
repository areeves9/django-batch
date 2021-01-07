from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.views.generic.edit import CreateView
from .forms import RegistrationForm

User = get_user_model()

class RegistrationView(CreateView):
    form_class = RegistrationForm
    template_name = 'registration/registration.html'



