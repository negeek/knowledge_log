from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class RegistrationForm(UserCreationForm):
    username = forms.CharField(min_length=5, label="Username", required=True)
    password1 = forms.CharField(
        min_length=8, label="Password", required=True, widget=forms.PasswordInput)
    password2 = forms.CharField(
        min_length=8, label="Confirm Password", required=True, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
