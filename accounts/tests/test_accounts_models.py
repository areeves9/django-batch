import pytest
from django.contrib.auth import get_user_model
from django.urls import resolve
from mixer.backend.django import Mixer

User = get_user_model()
mixer = Mixer(commit=False)

@pytest.fixture
def create_user():
    user = User.objects.create_user(email='jay@aol.com')
    yield user
    if user:
        user.delete()

@pytest.mark.django_db(transaction=True)
def test_create_user(create_user):
    assert create_user.email == 'jay@aol.com'

@pytest.mark.django_db(transaction=True)
def test_get_absolute_url(create_user):
    path = create_user.get_absolute_url()
    assert resolve(path).view_name == 'accounts:profile' 
    