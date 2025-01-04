from django import forms
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    """Form for submitting a contact message.

    This form is tied to the ContactMessage model and includes fields for the user to submit their name, email, subject, and message.
    """
    
    class Meta:
        # Define the model this form is based on
        model = ContactMessage
        
        # Specify the fields to be included in the form
        fields = ['name', 'email', 'subject', 'message']
