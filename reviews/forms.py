from django import forms
from core.utils import validate_max_length
from .models import Review

class ReviewForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add max length validation for review text
        self.fields['text'].validators.append(
            lambda value: validate_max_length(value, 300, 'Review text')
        )

    class Meta:
        # Define the model and fields to include in the form
        model = Review
        fields = ['rating', 'text']
        
        # Customize form widgets
        widgets = {
            # Rating field with a select dropdown for ratings 1 to 5
            'rating': forms.Select(choices=[(i, f'{i}★') for i in range(1, 6)]),
            
            # Text field with a placeholder and a row limit
            'text': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Write your review (max 300 characters)'
            })
        }
