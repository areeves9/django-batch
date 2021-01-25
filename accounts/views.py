from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import (
    get_user_model,
    authenticate,
    login
)
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from .forms import RegistrationForm, UserProfileUpdateForm

User = get_user_model()


class RegistrationFormView(SuccessMessageMixin, CreateView):
    '''
    Subclasses generic Django edit view CreateView.
    '''
    form_class = RegistrationForm
    template_name = 'registration/registration_form.html'
    success_message = 'Welcome to the site %(email)s!'

    def form_valid(self, form):
        valid = super().form_valid(form)
        username = form.cleaned_data['email']
        password = form.cleaned_data['password1']
        user = authenticate(self.request, username=username, password=password)
        login(self.request, user)
        return valid


class UserLoginView(SuccessMessageMixin, auth_views.LoginView):
    '''
    Subclasses LoginView from django.contrib.auth.
    '''
    redirect_authenticated_user = True
    success_message = 'Welcome back %(username)s!'

    def get_success_url(self):
        return reverse_lazy(
            'accounts:profile',
            kwargs={
                'unique_id': self.request.user.unique_id
            }
        )


class UserProfileView(LoginRequiredMixin, DetailView):
    '''
    Displays detail about a given SiteUser instance.
    '''
    model = User
    context_object_name = 'user'
    slug_field = 'unique_id'
    slug_url_kwarg = 'unique_id'
    template_name = 'registration/profile.html'


class UserProfileUpdateView(
    SuccessMessageMixin,
    UserPassesTestMixin,
    UpdateView
):
    '''
    Edits fields for a given SiteUser instance.
    '''
    model = User
    context_object_name = 'user'
    form_class = UserProfileUpdateForm
    slug_field = 'unique_id'
    slug_url_kwarg = 'unique_id'
    success_message = 'Profile Updated!'
    template_name = 'registration/user_profile_update_form.html'

    def test_func(self):
        return self.request.user.pk == self.get_object().pk


class UserPasswordChangeView(SuccessMessageMixin, auth_views.PasswordChangeView):
    success_message = 'Password changed successfully.'

    def get_success_url(self):
        return reverse_lazy(
            'accounts:profile',
            kwargs={
                'unique_id': self.request.user.unique_id
            }
        )
