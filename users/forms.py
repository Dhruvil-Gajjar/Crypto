from django import forms
from django.contrib.auth import (
    password_validation,
)
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordResetForm

from users.models import User, COMPANY_SIZE_CHOICES, SECTOR_CHOICES

COMPANY_SIZES = ((0, "-- Select Company Size --"),) + COMPANY_SIZE_CHOICES
SECTORS = ((0, "-- Select Sector --"),) + SECTOR_CHOICES


class SignupForm(UserCreationForm):
    email = forms.EmailField(
        max_length=200,
        help_text='Required',
        widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'E-Mail', 'required': True})
    )
    password1 = forms.CharField(
        help_text=password_validation.password_validators_help_text_html(),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Please enter a password'}), )
    password2 = forms.CharField(
        help_text="Enter the same password as before, for verification.",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Please re-enter your password.'}), )

    company_size = forms.ChoiceField(
        choices=COMPANY_SIZES, required=False,
        widget=forms.Select(attrs={'class': 'form-group form-control', 'required': True})
    )

    sector = forms.ChoiceField(
        choices=SECTORS, required=False,
        widget=forms.Select(attrs={'class': 'form-group form-control', 'required': True})
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password1', 'company_name', 'company_size', 
                  'sector', 'phone_number')
        widgets = {
            # 'first_name': forms.TextInput(attrs={'class': 'form-control border-top-0 border-right-0 border-left-0 rounded-0 shadow-none', 'placeholder': 'First Name', 'required': True}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name', 'required': True}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name', 'required': True}),
            'company_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company Name', 'required': True}),
            # 'company_size': forms.Select(attrs={'class': 'form-group form-control', 'placeholder': 'Company Size'}),
            # 'sector': forms.Select(attrs={'class': 'form-group form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone number', 'required': True})
        }


class RegisterForm(UserCreationForm):
    password1 = forms.CharField(
        help_text=password_validation.password_validators_help_text_html(),
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}), )
    password2 = forms.CharField(
        help_text="Enter the same password as before, for verification.",
        label="Confirm password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}), )

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "password1", "password2", "is_staff", "is_active", "is_superuser")
        widgets = {
            # 'username': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            # 'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            # 'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_superuser': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class EditUserForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "is_staff", "is_active", "is_superuser")
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_superuser': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class UpdateUserForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "company_name", "company_size", "sector", "phone_number")
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'company_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'company_size': forms.Select(attrs={'class': 'form-control'}),
            'sector': forms.Select(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ex) 01012345678 (without "-")'})
        }


class ResendActivationEmailForm(forms.Form):
    email = forms.EmailField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )


class UserPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(UserPasswordResetForm, self).__init__(*args, **kwargs)

    email = forms.EmailField(
        label='',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
