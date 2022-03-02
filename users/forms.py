from django import forms
from django.contrib.auth import (
    password_validation,
)
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from users.models import User


class SignupForm(UserCreationForm):
    email = forms.EmailField(
        max_length=200,
        help_text='Required',
        widget=forms.TextInput(
        attrs={'class': 'form-control border-top-0 border-right-0 border-left-0 rounded-0 shadow-none',
               'placeholder': 'E-Mail', 'required': True})
    )
    password1 = forms.CharField(
        help_text=password_validation.password_validators_help_text_html(),
        widget=forms.PasswordInput(attrs={'class': 'form-control border-top-0 border-right-0 border-left-0 rounded-0 shadow-none', 'placeholder': 'Enter password'}), )
    password2 = forms.CharField(
        help_text="Enter the same password as before, for verification.",
        widget=forms.PasswordInput(attrs={'class': 'form-control border-top-0 border-right-0 border-left-0 rounded-0 shadow-none', 'placeholder': 'Confirm password'}), )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password1')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control border-top-0 border-right-0 border-left-0 rounded-0 shadow-none', 'placeholder': 'First Name', 'required': True}),
            'last_name': forms.TextInput(attrs={'class': 'form-control border-top-0 border-right-0 border-left-0 rounded-0 shadow-none', 'placeholder': 'Last Name', 'required': True})
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
        fields = ("email", "first_name", "last_name",)
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
        }
