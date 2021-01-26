from accounts.tokens import account_activation_token
from accounts.forms import (
    RegistrationForm,
    UserProfileUpdateForm,
    UserPasswordResetForm,
    UserPasswordResetConfirmForm,
)
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import get_user_model, login
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
            success_message = 'Welcome to the site!'
            messages.success(request, success_message)
            return redirect(user.get_absolute_url())
        else:
            return render(request, 'registration/activation_invalid.html')


class RegistrationFormView(SuccessMessageMixin, CreateView):
    '''
    Subclasses generic Django edit view CreateView.
    Override the post method to email user confirmation
    URL containing uid and token.
    '''
    form_class = RegistrationForm
    template_name = 'registration/registration_form.html'

    def get_success_url(self):
        return reverse_lazy('accounts:registration_complete')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            to_email = form.cleaned_data['email']
            form.save()
            subject = 'Active your account.'
            current_site = get_current_site(request)
            message = render_to_string(
                'registration/activation_email.html',
                {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(form.instance.pk)),
                    'token': account_activation_token.make_token(form.instance),
                })
            email = EmailMessage(subject, message, to=[to_email, ])
            email.send()
            success_message = f'Activation link sent to {user}'
            messages.success(request, success_message)
            return redirect(self.get_success_url())
        else:
            form = self.form_class()
            return form


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


class UserPasswordChangeView(
    SuccessMessageMixin,
    auth_views.PasswordChangeView
):
    '''
    User changes password by a link located
    on their profile page.
    '''
    # form_class = UserPasswordChangeForm
    success_message = 'Password changed successfully.'

    def get_success_url(self):
        return reverse_lazy(
            'accounts:profile',
            kwargs={
                'unique_id': self.request.user.unique_id
            }
        )


class UserPasswordResetView(
    SuccessMessageMixin,
    auth_views.PasswordResetView
):
    '''
    User enters email in form field and server
    sends an email containing a URL where the user
    can enter a new password.
    '''
    form_class = UserPasswordResetForm

    def get_success_url(self):
        return reverse_lazy('password_reset_complete')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            success_message = f'Password for {email} successfully updated!'
            messages.success(request, success_message)
            return redirect(self.get_success_url())
        else:
            form = self.form_class()
            return form


class UserPasswordResetConfirmView(
    SuccessMessageMixin,
    auth_views.PasswordResetConfirmView
):
    '''
    User enters new password and confirms.
    '''
    form_class = UserPasswordResetConfirmForm
    success_message = 'Your password has been updated!'
