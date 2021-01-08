from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm
)
from django.contrib.auth import get_user_model
from crispy_forms.helper import FormHelper

User = get_user_model()

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    username = forms.EmailField(
        label='', 
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control', 
                'placeholder': 'Email', 
                'id': 'hello'
                }
            )
        )
    
    password = forms.CharField(
        label='', 
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control', 
                'placeholder': 'Password', 
                'id': 'hi',
                }
            )
        )


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        label='',
        widget=forms.EmailInput
    )
    password1 = forms.CharField(
        label='', 
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label='', 
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
