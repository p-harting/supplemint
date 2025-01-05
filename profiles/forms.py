from django import forms
from .models import UserProfile

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
            # Add required field indicator to placeholder if field is required
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]
            
            # Set placeholder and CSS class for each field
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            
            # Remove auto-generated label and set custom label
            self.fields[field].label = placeholders[field]
