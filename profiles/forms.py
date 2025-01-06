from django import forms
from django.utils.safestring import mark_safe
from .models import UserProfile
from core.utils import validate_email, validate_max_length

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        # Fields to be included in the form
        fields = ('full_name', 'email', 'phone_number',
                 'street_address1', 'street_address2',
                 'town_or_city', 'postcode', 'country',
                 'county',)

    def __init__(self, *args, **kwargs):
        """
        Customize form fields by adding placeholders, classes, and autofocus.
        Also removes auto-generated labels and adjusts placeholder text.
        """
        super().__init__(*args, **kwargs)
        
        # Define placeholders for each field
        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'country': 'Country',
            'postcode': 'Postal Code',
            'town_or_city': 'Town or City',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2',
            'county': 'County, State or Locality',
        }

        # Set autofocus on the first field
        self.fields['full_name'].widget.attrs['autofocus'] = True
        
        # Iterate through all fields to set placeholders, CSS classes, and labels
        for field in self.fields:
            # Add required field indicator and red star
            if field in ['full_name', 'email', 'phone_number', 'street_address1', 'town_or_city', 'postcode', 'country']:
                placeholder = f'{placeholders[field]} *'
                self.fields[field].label = mark_safe(f'{placeholders[field]} <span class="required-star">*</span>')
            else:
                placeholder = placeholders[field]
                self.fields[field].label = placeholders[field]
                self.fields[field].required = False
            
            # Set placeholder and CSS class for each field
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            
            # Add maxlength attributes and validation based on model field lengths
            if field == 'full_name':
                self.fields[field].widget.attrs['maxlength'] = '50'
                self.fields[field].validators.append(
                    lambda value: validate_max_length(value, 50, 'Full name')
                )
            elif field == 'email':
                self.fields[field].widget.attrs['maxlength'] = '254'
                self.fields[field].validators.append(
                    lambda value: validate_max_length(value, 254, 'Email')
                )
            elif field == 'phone_number':
                self.fields[field].widget.attrs['maxlength'] = '20'
                self.fields[field].validators.append(
                    lambda value: validate_max_length(value, 20, 'Phone number')
                )
            elif field == 'country':
                self.fields[field].widget.attrs['maxlength'] = '40'
                self.fields[field].validators.append(
                    lambda value: validate_max_length(value, 40, 'Country')
                )
            elif field == 'postcode':
                self.fields[field].widget.attrs['maxlength'] = '20'
                self.fields[field].validators.append(
                    lambda value: validate_max_length(value, 20, 'Postcode')
                )
            elif field == 'town_or_city':
                self.fields[field].widget.attrs['maxlength'] = '40'
                self.fields[field].validators.append(
                    lambda value: validate_max_length(value, 40, 'Town or city')
                )
            elif field == 'street_address1':
                self.fields[field].widget.attrs['maxlength'] = '80'
                self.fields[field].validators.append(
                    lambda value: validate_max_length(value, 80, 'Street address 1')
                )
            elif field == 'street_address2':
                self.fields[field].widget.attrs['maxlength'] = '80'
                self.fields[field].validators.append(
                    lambda value: validate_max_length(value, 80, 'Street address 2')
                )
            elif field == 'county':
                self.fields[field].widget.attrs['maxlength'] = '80'
                self.fields[field].validators.append(
                    lambda value: validate_max_length(value, 80, 'County')
                )
