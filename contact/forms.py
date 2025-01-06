from django import forms
from core.utils import (
    validate_max_length,
    validate_email
)
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    """Form for submitting a contact message.

    This form is tied to the ContactMessage model and includes fields for the user to submit their name, email, subject, and message.
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Mark all fields as required with red stars
        required_fields = ['name', 'email', 'subject', 'message']
        for field_name in required_fields:
            if field_name in self.fields:
                self.fields[field_name].label_suffix = ' *'
                self.fields[field_name].label_attrs = {'class': 'required-star'}
        
        # Add field-specific validations
        self.fields['name'].validators.append(
            lambda value: validate_max_length(value, 100, 'Name')
        )
        self.fields['email'].validators.append(
            lambda value: validate_email(value)
        )
        self.fields['subject'].validators.append(
            lambda value: validate_max_length(value, 200, 'Subject')
        )
        self.fields['message'].validators.append(
            lambda value: validate_max_length(value, 2000, 'Message')
        )

    class Meta:
        # Define the model this form is based on
        model = ContactMessage
        
        # Specify the fields to be included in the form
        fields = ['name', 'email', 'subject', 'message']
        
        # Customize form widgets
        widgets = {
            'message': forms.Textarea(attrs={'rows': 5}),
        }
