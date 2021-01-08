from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import views, get_user_model
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import FormView, CreateView
from .forms import LoginForm, RegistrationForm

User = get_user_model()

class RegistrationView(CreateView):
    form_class = RegistrationForm
    template_name = 'registration/registration.html'