from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm, SetPasswordForm, PasswordResetForm
from django.contrib.auth.models import User
from .models import Customer

# Login form, inheriting from AuthenticationForm to handle user login functionality
class LoginForm(AuthenticationForm):
    # Customizing the username field with additional HTML attributes for styling
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    # Customizing the password field with additional HTML attributes for styling
    password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class': 'form-control'}))

# User registration form that inherits from UserCreationForm
class CustomerRegistrationForm(UserCreationForm):
    # Customizing the username field for styling and autofocus
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    # Customizing the email field for styling
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    # Customizing the password fields for styling
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    # Meta class to define the model and fields to be used in the form
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# Password change form, inheriting from PasswordChangeForm
class MyPasswordChangeForm(PasswordChangeForm):
    # Customizing the old password field with additional HTML attributes for styling
    old_password = forms.CharField(label='Old Password', widget=forms.PasswordInput(attrs={
        'autofocus': 'True', 'autocomplete': 'current-password', 'class': 'form-control'}))
    # Customizing the new password field for styling
    new_password1 = forms.CharField(label='New Password', widget=forms.PasswordInput(attrs={
        'autocomplete': 'current-password', 'class': 'form-control'}))
    # Customizing the confirm new password field for styling
    new_password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={
        'autocomplete': 'current-password', 'class': 'form-control'}))

# Password reset form, inheriting from PasswordResetForm
class MyPasswordResetForm(PasswordResetForm):
    # Customizing the email field for styling
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))

# Set new password form, inheriting from SetPasswordForm
class MySetPasswordForm(SetPasswordForm):
    # Customizing the new password field for styling
    new_password1 = forms.CharField(label='New Password', widget=forms.PasswordInput(attrs={
        'autocomplete': 'current-password', 'class': 'form-control'}))
    # Customizing the confirm new password field for styling
    new_password2 = forms.CharField(label='Confirm New Password', widget=forms.PasswordInput(attrs={
        'autocomplete': 'current-password', 'class': 'form-control'}))

# Customer profile form, inheriting from forms.ModelForm to handle profile data
class CustomerProfileForm(forms.ModelForm):
    # Meta class to define the model and fields to be used in the form
    class Meta:
        model = Customer
        fields = ['name', 'locality', 'city', 'mobile', 'state', 'zipcode']
        # Customizing the form fields with widgets for styling
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),  # Name field styling
            'locality': forms.TextInput(attrs={'class': 'form-control'}),  # Locality field styling
            'city': forms.TextInput(attrs={'class': 'form-control'}),  # City field styling
            'mobile': forms.NumberInput(attrs={'class': 'form-control'}),  # Mobile field styling
            'state': forms.Select(attrs={'class': 'form-control'}),  # State dropdown styling
            'zipcode': forms.NumberInput(attrs={'class': 'form-control'}),  # Zipcode field styling
        }
