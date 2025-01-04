from django import forms
from .models import Product

# Form for Product model
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),  # Short description
            'detailed_description': forms.Textarea(attrs={'rows': 5}),  # Longer description
            'nutritional_info': forms.Textarea(attrs={'rows': 5}),  # Nutritional info
            'how_to_use': forms.Textarea(attrs={'rows': 3}),  # Instructions
        }
