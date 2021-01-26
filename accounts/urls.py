from accounts import views
from django.urls import path
from django.views.generic.base import TemplateView
from django.contrib.auth import views as auth_views
from accounts.forms import (
    LoginForm,
    UserPasswordChangeForm,
    UserPasswordResetForm,
)

app_name = 'accounts'

urlpatterns = [
    path(
        'activate/<uidb64>/<token>/',
        views.Activate.as_view(),
        name='activate'
    ),
    path(
        'login', views.UserLoginView.as_view(
            form_class=LoginForm
        ), name='login'
    ),
    path(
        'logout', auth_views.LogoutView.as_view(
            template_name='registration/logged_out.html'
        ), name='logout'
    ),
    path(
        'register',
        views.RegistrationFormView.as_view(),
        name='register'
    ),
    path(
        'password/change',
        views.UserPasswordChangeView.as_view(
            form_class=UserPasswordChangeForm
        ),
        name='password_change'
    ),
    path(
        'password/reset',
        views.UserPasswordResetView.as_view(
            form_class=UserPasswordResetForm
        ), name='password_reset'
    ),
    path(
        'password/reset/<uidb64>/<token>/confirm/',
        views.UserPasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
    ),
    path(
        'profile/<uuid:unique_id>/',
        views.UserProfileView.as_view(
            template_name='accounts/profile.html'
        ), name='profile'
    ),
    path(
        'profile/<uuid:unique_id>/update/',
        views.UserProfileUpdateView.as_view(
            template_name='accounts/user_profile_update_form.html'
        ), name='profile_update'
    ),
    path(
        'registration/complete/',
        TemplateView.as_view(
            template_name='registration/registration_complete.html'
        ), name='registration_complete'
    )
]
