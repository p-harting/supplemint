from django import forms
from .models import Product, Category, SubCategory

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'detailed_description': forms.Textarea(attrs={'rows': 5}),
            'nutritional_info': forms.Textarea(attrs={'rows': 5}),
            'how_to_use': forms.Textarea(attrs={'rows': 3}),
        }