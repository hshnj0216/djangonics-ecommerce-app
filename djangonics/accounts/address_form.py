from django import forms
from .models import Address

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            'recipient_name',
            'street_address',
            'apartment_address',
            'city',
            'state',
            'zip_code',
            'phone_number',
            'is_default',
        ]
        labels = {
            'recipient_name': 'Recipient Name',
            'street_address': 'Street Address',
            'apartment_address': 'Apartment or Suite',
            'city': 'City',
            'state': 'State',
            'zip_code': 'ZIP Code',
            'phone_number': 'Phone Number',
            'is_default': 'Set as Default',
        }

    def clean_recipient_name(self):
        recipient_name = self.cleaned_data.get('recipient_name')
        if not recipient_name.isalpha():
            raise forms.ValidationError('Recipient name should only contain letters')
        return recipient_name

    def clean_street_address(self):
        street_address = self.cleaned_data.get('street_address')
