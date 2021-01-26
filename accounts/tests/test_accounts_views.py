import pytest
from mixer.backend.django import Mixer
from django.test import RequestFactory
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
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
    response = UserProfileView.as_view()(request=request, unique_id=request.user.unique_id)
    assert response.template_name == ['registration/profile.html']


def test_redirect_anonymous_to_login_from_profile():
    path = reverse('accounts:profile', kwargs={'unique_id': '8db49825-244b-4ee9-a857-4da3cf40f380'})
    user = AnonymousUser()
    factory = RequestFactory()
    request = factory.get(path)
    request.user = user
    response = UserProfileView.as_view()(request, unique_id='8db49825-244b-4ee9-a857-4da3cf40f380')
    assert response.url == '/accounts/login?next=/accounts/profile/8db49825-244b-4ee9-a857-4da3cf40f380/'