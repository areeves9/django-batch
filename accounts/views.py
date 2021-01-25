from accounts.tokens import account_activation_token
from .forms import RegistrationForm, UserProfileUpdateForm
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import (
    get_user_model,
    authenticate,
    login
)
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView

User = get_user_model()


class Activate(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            # activate user and login:
            user.is_active = True
            user.save()
            login(request, user)
            return redirect(user.get_absolute_url())
        else:
            return render(request, 'registration/activation_invalid.html')


class RegistrationFormView(SuccessMessageMixin, CreateView):
    '''
    Subclasses generic Django edit view CreateView.
    '''
    form_class = RegistrationForm
    template_name = 'registration/registration_form.html'
    success_url = 'registration/registration_complete.html'
    success_message = 'Please check your email, %(email)s, for confirmation.'

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
