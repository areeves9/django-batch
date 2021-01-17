import pytest
from django.test import RequestFactory, Client
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser
from accounts.views import RegistrationFormView

def test_get_registration_view():
    path = reverse('accounts:register')
    factory = RequestFactory()
    user = AnonymousUser()
    request = factory.get(path)
    request.user = user
    response = RegistrationFormView(request=request)
    assert response.template_name == 'registration/registration_form.html'

@pytest.mark.django_db(transaction=True)
def test_post_registration_view():
    path = reverse('accounts:register')
    c = Client()
    factory = RequestFactory()
    user = AnonymousUser()
    data = {
        'email': 'jza@aol.com', 
        'password1': '16zs_90!mm416', 
        'password2': '16zs_90!mm416'
    }
    request = factory.post(path, data)
    request.session = c.session
    request.user = user
    response = RegistrationFormView.as_view()(request=request)
    assert response.url == reverse(
        'accounts:profile', 
        kwargs={'pk': request.user.pk}
    )
