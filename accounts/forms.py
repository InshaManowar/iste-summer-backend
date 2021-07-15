from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from accounts.models import Account


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': 'email'}),
        label=''
    )
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'first name'}),
        label=''
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'last name'}),
        label=''
    )
    registration_number = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Registration Number'}),
        label=''
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Password'}),
        label=''
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
        label=''
    )

    class Meta:
        model = Account
        fields = ("first_name", "last_name", "email",
                  'password1', 'password2', 'registration_number')

    def save(self, *args, **kwargs):
        account = super().save(commit=False, *args, **kwargs)
        account.registration_number = self.cleaned_data['registration_number']
        account.save()
        return account


class AccountAuthenticationForm(forms.ModelForm):
    password = forms.CharField(
        label=None, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    email = forms.CharField(label=None, widget=forms.TextInput(
        attrs={'class': 'form-control'}))

    class Meta:
        model = Account
        fields = ('email', 'password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("invalid login")
