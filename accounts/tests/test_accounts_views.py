import pytest
from django.urls import reverse
from django.test import RequestFactory, Client
from django.contrib.auth import get_user_model
from accounts.views import RegistrationView, UserDetailView
from mixer.backend.django import Mixer

User = get_user_model()
mixer = Mixer(commit=False)

@pytest.mark.django_db(transaction=True)
def test_user_registration():
    path = reverse('accounts:register')
    client = Client()
    request = RequestFactory().get(path)
    request.session = client.session
    request.user = mixer.blend(User, email='theboss@aol.com')
    response = RegistrationView(request=request)
    assert request.user.get_absolute_url() == response.success_url() 