from django import forms
from core.utils import (
    validate_max_length,
    validate_numeric,
    validate_positive_number
)
from .models import Product


# Form for Product model
class ProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only mark these specific fields as required
        required_fields = ['name', 'description', 'base_price', 'stock']
        for field_name in required_fields:
            if field_name in self.fields:
                self.fields[field_name].label_suffix = ' *'
                self.fields[field_name].label_attrs = (
                    {'class': 'required-star'})
        # Add field-specific validations
        self.fields['name'].validators.append(
            lambda value: validate_max_length(value, 254, 'Name')
        )
        self.fields['description'].validators.append(
            lambda value: validate_max_length(value, 2000, 'Description')
        )
        self.fields['base_price'].validators.extend([
            lambda value: validate_numeric(value, 'Price'),
            lambda value: validate_positive_number(value, 'Price')
        ])
        self.fields['stock'].validators.extend([
            lambda value: validate_numeric(value, 'Stock'),
            lambda value: validate_positive_number(value, 'Stock')
        ])

    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'detailed_description': forms.Textarea(attrs={'rows': 5}),
            'nutritional_info': forms.Textarea(attrs={'rows': 5}),
            'how_to_use': forms.Textarea(attrs={'rows': 3}),
        }
