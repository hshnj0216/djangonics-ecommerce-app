from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator, RegexValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import ModelForm
from accounts.models import User
import re


class SignUpForm(forms.ModelForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Email'}),
        validators=[EmailValidator()],
        error_messages={
            'unique': _("This email is already registered."),
        },
    )
    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'First Name'}),
        validators=[
            RegexValidator(r'^[a-zA-Z\s]*$', _("First name should only contain alphabets and spaces.")),
        ],
    )
    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Last Name'}),
        validators=[
            RegexValidator(r'^[a-zA-Z\s]*$', _("Last name should only contain alphabets and spaces.")),
        ],
    )
    contact_number = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Contact Number (123-456-7890)'}),
        validators=[
            RegexValidator(r"^(1-)?\d{3}-\d{3}-\d{4}$", _("Invalid US phone number. The format should be: 123-456-7890 or 1-123-456-7890")),
        ],
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
        validators=[
            RegexValidator(r'^[a-zA-Z0-9]{8,}$', _("Password should be at least 8 characters long and should only contain alphanumeric characters.")),
        ],
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'contact_number', 'password']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                self.fields['email'].error_messages['unique'],
                code='unique',
            )
        return email

    def clean_contact_number(self):
        contact_number = self.cleaned_data.get('contact_number')
        if User.objects.filter(contact_number=contact_number).exists():
            raise ValidationError("Contact number already exists.")
        return contact_number



class LoginForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput)
    password = forms.CharField(widget=forms.PasswordInput)

