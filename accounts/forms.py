from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
    UserCreationForm,
)
from django.contrib.auth import get_user_model


User = get_user_model()


class UserPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    email = forms.EmailField(
        label='',
        widget=forms.EmailInput(
            attrs={
                'class': 'emailinput form-control',
                'placeholder': 'Email',
                'id': 'input-email-password-change'
                }
            )
        )


class UserProfileUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    first_name = forms.CharField(
        label='',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'First Name',
                'id': 'input-first-name'
                }
            )
        )

    last_name = forms.CharField(
        label='',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Last Name',
                'id': 'input-last-name'
                }
            )
        )

    class Meta:
        model = User
        fields = ('first_name', 'last_name',)


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    username = forms.EmailField(
        label='',
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Email',
                'id': 'input-username'
                }
            )
        )

    password = forms.CharField(
        label='',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control', 
                'placeholder': 'Password', 
                'id': 'input-password',
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


class UserPasswordChangeForm(PasswordChangeForm):
    '''
    Add helper text for new_password1.
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    old_password = forms.CharField(
            label='',
            widget=forms.PasswordInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Previous Password',
                    'id': 'input-first-name'
                    }
                )
            )
    new_password1 = forms.CharField(
            label='',
            help_text='<ul><li>Your password can’t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can’t be a commonly used password.</li><li>Your password can’t be entirely numeric.</li></ul>',
            widget=forms.PasswordInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'New Password',
                    'id': 'input-first-name'
                    }
                )
            )

    new_password2 = forms.CharField(
            label='',
            widget=forms.PasswordInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'New Password Confirm',
                    'id': 'input-first-name'
                    }
                )
            )

    class Meta:
        model = User


class UserPasswordResetConfirmForm(SetPasswordForm):
    '''
    Add helper text for new_password1.
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    new_password1 = forms.CharField(
            label='',
            help_text='<ul><li>Your password can’t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can’t be a commonly used password.</li><li>Your password can’t be entirely numeric.</li></ul>',
            widget=forms.PasswordInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'New Password',
                    'id': 'input-first-name'
                    }
                )
            )

    new_password2 = forms.CharField(
            label='',
            widget=forms.PasswordInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'New Password Confirm',
                    'id': 'input-first-name'
                    }
                )
            )
