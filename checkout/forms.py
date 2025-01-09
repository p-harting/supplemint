from django import forms
from django.utils.safestring import mark_safe
from django_countries import countries
from .models import Order
from core.utils import validate_email, validate_max_length


class OrderForm(forms.ModelForm):
    # Country field with a custom widget and class
    country = forms.ChoiceField(
        choices=countries,
        widget=forms.Select(attrs={
            'class': 'stripe-style-input country-select'
        })
    )

    class Meta:
        model = Order
        fields = ('full_name', 'email', 'phone_number',
                  'street_address1', 'street_address2',
                  'town_or_city', 'postcode', 'country',
                  'county',)

    def __init__(self, *args, **kwargs):
        """
        Initialize the form by adding placeholders,
        classes, removing auto-generated labels,
        and setting autofocus on the first field.
        """
        self.user = kwargs.pop('user', None)  # Get user if passed
        super().__init__(*args, **kwargs)
        # Define placeholder text for each field
        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'country': 'Country',
            'postcode': 'Postal Code (optional)',
            'town_or_city': 'Town or City',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2 (optional)',
            'county': 'County, State or Locality (optional)',
        }

        # Set autofocus on the first field (full_name)
        self.fields['full_name'].widget.attrs['autofocus'] = True
        # Iterate over all fields to set placeholders, classes, and aria-labels
        for field in self.fields:
            if field in ['full_name', 'email', 'phone_number', 'country',
                         'town_or_city', 'street_address1']:
                placeholder = f'{placeholders[field]} *'
                self.fields[field].widget.attrs['placeholder'] = placeholder
                self.fields[field].label = mark_safe(
                    f'{placeholders[field]}'
                    f'<span class="required-star">*</span>')
            else:
                placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
                self.fields[field].label = placeholders[field]
                self.fields[field].required = False
            # Exclude country field from stripe-style-input class
            if field != 'country':
                self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].widget.attrs['aria-label'] = placeholders[field]
            # Maxlength attributes and validation based on model field lengths
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
                    lambda value: validate_max_length(
                        value, 20, 'Phone number')
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
                    lambda value: validate_max_length(
                        value, 40, 'Town or city')
                )
            elif field == 'street_address1':
                self.fields[field].widget.attrs['maxlength'] = '80'
                self.fields[field].validators.append(
                    lambda value: validate_max_length(
                        value, 80, 'Street address 1')
                )
            elif field == 'street_address2':
                self.fields[field].widget.attrs['maxlength'] = '80'
                self.fields[field].validators.append(
                    lambda value: validate_max_length(
                        value, 80, 'Street address 2')
                )
            elif field == 'county':
                self.fields[field].widget.attrs['maxlength'] = '80'
                self.fields[field].validators.append(
                    lambda value: validate_max_length(value, 80, 'County')
                )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not validate_email(email):
            raise forms.ValidationError('Please enter a valid email address')
        return email
