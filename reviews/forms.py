from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'text']
        widgets = {
            'rating': forms.Select(choices=[(i, f'{i}★') for i in range(1, 6)]),
            'text': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Write your review (max 300 characters)'
            })
        }