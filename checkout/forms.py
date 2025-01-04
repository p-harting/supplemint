from django import forms
from django_countries import countries
from .models import Order


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
            'postcode': 'Postal Code',
            'town_or_city': 'Town or City',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2',
            'county': 'County, State or Locality',
        }

        # Set autofocus on the first field (full_name)
        self.fields['full_name'].widget.attrs['autofocus'] = True
        
        # Iterate over all fields to set placeholders, classes, and aria-labels
        for field in self.fields:
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'  # Add * for required fields
            else:
                placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            if field != 'country':  # Exclude country field from stripe-style-input class
                self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].widget.attrs['aria-label'] = placeholders[field]
            self.fields[field].label = False  # Remove labels
