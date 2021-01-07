from . import views
from django.urls import path
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
    path('login', auth_views.LoginView.as_view(), name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('register', views.RegistrationView.as_view(), name='register'),
]
