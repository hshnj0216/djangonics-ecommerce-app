from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator, RegexValidator
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import ModelForm
from accounts.models import User
import re

def validate_password(value):
    """Check if password meets the requirements."""
    if len(value) < 8:
        raise ValidationError("Password should be at least 8 characters long.")
    if " " in value:
        raise ValidationError("Password should not contain spaces.")
    if not value:
        raise ValidationError("Password should not be empty.")
    if not re.match('^[a-zA-Z0-9]*$', value):
        raise ValidationError("Password should only contain alphanumeric characters.")

def validate_first_name(value):
    # Validate first_name
    if not value:
        raise ValidationError("First name must not be empty.")
    if len(value) > 100:
        raise ValidationError("First name must not exceed 100 characters.")
    if not value.replace(" ", "").isalpha():
        raise ValidationError("First name should only contain alphabets and spaces.")

def validate_last_name(value):
    if not value:
        raise ValidationError("Last name must not be empty.")
    if len(value) > 100:
        raise ValidationError("Last name must not exceed 100 characters.")
    if not value.replace(" ", "").isalpha():
        raise ValidationError("Last name should only contain alphabets and spaces.")

def validate_email(value):
    validator = EmailValidator()
    try:
        validator(value)
    except ValidationError:
        raise ValidationError("Invalid email address.")

def validate_contact_number(value):
    pattern = re.compile(r"^(1-)?\d{3}-\d{3}-\d{4}$")
    if not pattern.match(value):
        raise ValidationError("Invalid US phone number. The format should be: 123-456-7890 or 1-123-456-7890")



class SignUpForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput, validators=[validate_first_name])
    last_name = forms.CharField(widget=forms.TextInput, validators=[validate_last_name])
    email = forms.CharField(widget=forms.EmailInput, validators=[validate_email])
    contact_number = forms.CharField(widget=forms.TextInput, validators=[validate_contact_number])
    password = forms.CharField(widget=forms.PasswordInput, validators=[validate_password])


class LoginForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput)
    password = forms.CharField(widget=forms.PasswordInput)

