"""Users forms."""

# Django
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

# Models
from .models import Profile


class UserForm(UserCreationForm):
    """Form that uses to handle user creation."""

    first_name = forms.CharField(
        max_length=30, required=True, 
        widget=forms.TextInput(attrs={'placeholder': '*Your first name.'}))
    
    last_name = forms.CharField(
        max_length=30, required=True,
        widget=forms.TextInput(attrs={'placeholder': '*Your last name.'}))

    username = forms.EmailField(
        max_length=255, required=True, 
        widget=forms.TextInput(attrs={'placeholder': '*Your email.'}))

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': '*Password.'}))

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': '*Confirm Password.'}))

    # reCaptcha token
    token = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        """Meta options."""
        model = User
        fields = (
            'first_name', 'last_name', 
            'username', 'password1', 
            'password2')


class AuthForm(AuthenticationForm):
    """Form that uses to handle user auth."""

    username = forms.EmailField(
        max_length=255, required=True, 
        widget=forms.TextInput(attrs={'placeholder': '*Email.'}))
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': '*Password.'}))

    class Meta:
        """Meta options."""
        model = User
        fields = ('username', 'password')


class ProfileForm(forms.ModelForm):
    """Profile form."""

    address = forms.CharField(
        max_length=100, required=True, widget=forms.HiddenInput())
    
    town = forms.CharField(
        max_length=100, required=True, widget=forms.HiddenInput())
    
    county = forms.CharField(
        max_length=100, required=True, widget=forms.HiddenInput())

    country = forms.CharField(
        max_length=60, required=True, widget=forms.HiddenInput())

    post_code = forms.CharField(
        max_length=8, required=True, widget=forms.HiddenInput())
    
    longitude = forms.CharField(
        max_length=50, required=True, widget=forms.HiddenInput())

    latitude = forms.CharField(
        max_length=50, required=True, widget=forms.HiddenInput())

    class Meta:
        """Meta options."""
        model = Profile
        fields = (
            'address', 'town', 
            'county','country', 
            'post_code', 'longitude', 
            'latitude')