from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import (
    views,
    get_user_model,
    authenticate,
    login
)
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import FormView, CreateView
from django.views.generic.detail import DetailView
from .forms import LoginForm, RegistrationForm

User = get_user_model()

class RegistrationFormView(SuccessMessageMixin, CreateView):
    form_class = RegistrationForm
    template_name = 'registration/registration_form.html'
    success_message = 'Welcome to the site %(email)s!'

    def form_valid(self, form):
        valid = super().form_valid(form)
        username = form.cleaned_data['email']
        password = form.cleaned_data['password1']
        user = authenticate(
            self.request, 
            username=username, 
            password=password
        )
        login(self.request, self.object)
        return valid

class UserDetailView(DetailView):
    model = User
    context_object_name = 'user'
    template_name = 'registration/profile.html'
