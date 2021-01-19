import pytest
from mixer.backend.django import Mixer
from django.test import RequestFactory, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.contrib.messages import get_messages
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from accounts.views import UserDetailView, RegistrationFormView

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
        'email': 'jza@aol.com',
        'password1': '16zs_90!mm416',
        'password2': '16zs_90!mm416',
    }
    response = c.post(path, data)
    messages = list(get_messages(response.wsgi_request))
    assert str(messages[0]) == 'Welcome to the site jza@aol.com!'


def test_get_userdetailview():
    user = mixer.blend(User, pk=10)
    path = reverse('accounts:profile', kwargs={'pk': user.pk})
    factory = RequestFactory()
    request = factory.get(path)
    request.user = user
    response = UserDetailView(request=request)
    assert response.template_name == 'registration/profile.html'
