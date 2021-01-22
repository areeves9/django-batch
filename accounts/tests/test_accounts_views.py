import pytest
from mixer.backend.django import Mixer
from django.test import RequestFactory, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.contrib.messages import get_messages
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from accounts.views import UserProfileView, RegistrationFormView

User = get_user_model()
mixer = Mixer(commit=False, fake=True)


def test_get_registrationview():
    path = reverse('accounts:register')
    factory = RequestFactory()
    user = AnonymousUser()
    request = factory.get(path)
    request.user = user
    response = RegistrationFormView(request=request)
    assert response.template_name == 'registration/registration_form.html'


@pytest.mark.django_db(transaction=True)
def test_post_registrationview():
    path = reverse('accounts:register')
    factory = RequestFactory()
    user = AnonymousUser()
    data = {
        'email': 'jza@aol.com',
        'password1': '16zs_90!mm416',
        'password2': '16zs_90!mm416',
    }
    request = factory.post(path, data)
    request.user = user
    middleware = SessionMiddleware(object)
    middleware.process_request(request)
    request.session.save()
    middleware = MessageMiddleware(object)
    middleware.process_request(request)
    request.session.save()
    response = RegistrationFormView.as_view()(request=request)
    assert response.url == reverse(
        'accounts:profile',
        kwargs={'pk': request.user.pk}
    )


@pytest.mark.django_db(transaction=True)
def test_post_registrationview_success_message():
    path = reverse('accounts:register')
    c = Client()
    data = {
        'email': 'az@gmail.com',
        'password1': '16zs_90!mm416',
        'password2': '16zs_90!mm416',
    }
    response = c.post(path, data)
    messages = list(get_messages(response.wsgi_request))
    assert str(messages[0]) == 'Welcome to the site az@gmail.com!'


@pytest.mark.django_db(transaction=True)
def test_post_loginview_success_message():
    path = reverse('accounts:login')
    c = Client()
    user = User.objects.create_user(email='az@gmail.com')
    user.set_password('waterwater12')
    user.save()
    data = {
        'username': 'az@gmail.com',
        'password': 'waterwater12',
    }
    response = c.post(path, data=data)
    messages = list(get_messages(response.wsgi_request))
    assert str(messages[0]) == f'Welcome back {user.email}!'


@pytest.fixture
@pytest.mark.django_db(transaction=True)
def user():
    user = mixer.blend(User)
    return User.objects.create_user(
        email=f'{user.email}',
        password='password123'
    )


@pytest.mark.django_db(transaction=True)
def test_get_userprofileview(user):
    factory = RequestFactory()
    path = user.get_absolute_url()
    request = factory.get(path)
    request.user = user
    response = UserProfileView.as_view()(request=request, pk=request.user.pk)
    assert response.template_name == ['registration/profile.html']


def test_redirect_anonymous_to_login_from_profile():
    path = reverse('accounts:profile', kwargs={'pk': 10})
    user = AnonymousUser()
    factory = RequestFactory()
    request = factory.get(path)
    request.user = user
    response = UserProfileView.as_view()(request, pk=10)
    assert response.url == '/accounts/login?next=/accounts/profile/10/'


@pytest.mark.django_db(transaction=True)
def test_redirect_authenticated_to_profile_from_login(user):
    path = reverse('accounts:login')
    c = Client()
    user.set_password('waterwater12')
    user.save()
    data = {
        'username': user.email,
        'password': 'waterwater12',
    }
    response = c.post(path, data=data)
    assert response.url == user.get_absolute_url()
