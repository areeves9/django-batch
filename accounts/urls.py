from . import views
from django.urls import path
from django.contrib.auth import views as auth_views
from accounts.forms import LoginForm

app_name = 'accounts'

urlpatterns = [
    path('login', auth_views.LoginView.as_view(
        form_class=LoginForm
        ), name='login'),
    path('logout', auth_views.LogoutView.as_view(
        template_name='registration/logged_out.html'
        ), name='logout'),
    path('register', views.RegistrationView.as_view(), name='register'),
    path('profile/<int:pk>/', views.UserDetailView.as_view(), name='profile'),
]
