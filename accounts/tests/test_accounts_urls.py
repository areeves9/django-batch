from django.urls import reverse, resolve


class TestUrls:
    def test_login_url(self):
        path = reverse('accounts:login')
        assert resolve(path).view_name == 'accounts:login'

    def test_logout_url(self):
        path = reverse('accounts:logout')
        assert resolve(path).view_name == 'accounts:logout'

    def test_register_url(self):
        path = reverse('accounts:register')
        assert resolve(path).view_name == 'accounts:register'

    def test_profile_url(self):
        path = reverse('accounts:profile', kwargs={'unique_id': '8db49825-244b-4ee9-a857-4da3cf40f380'})
        assert resolve(path).view_name == 'accounts:profile'
