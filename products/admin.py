from django.contrib import admin
from django.core.exceptions import ValidationError
from .models import Product, Category, SubCategory, ProductSize, Sale

# Inline for managing product sizes
class ProductSizeInline(admin.TabularInline):
    model = ProductSize
    extra = 1
    fields = ('name', 'price', 'stock')

    def clean(self):
        """Validate that stock is not negative for each size"""
        super().clean()
        for form in self.forms:
            if not form.cleaned_data or form.cleaned_data.get('DELETE'):
                continue
            stock = form.cleaned_data.get('stock', 0)
            if stock < 0:
                form.add_error('stock', 'Stock cannot be negative')

# Product admin configuration
class ProductAdmin(admin.ModelAdmin):
    def clean(self):
        """Validate that stock is not negative"""
        super().clean()
        if self.cleaned_data.get('stock', 0) < 0:
            raise ValidationError('Stock cannot be negative')

    # List of fields to display in the product list view
    list_display = (
        'sku', 'name', 'category', 'subcategory', 'base_price', 
        'get_sale_display', 'get_stock_display', 'rating', 'image', 
        'seo_title', 'seo_meta_description',
    )
    
    # Fields to display in the form for adding/editing a product
    fields = (
        'sku', 'name', 'category', 'subcategory', 'description', 'detailed_description', 
        'nutritional_info', 'how_to_use', 'key_facts', 'has_sizes', 'base_price', 'sale', 
        'stock', 'rating', 'image', 'slug', 'seo_title', 'seo_meta_description', 'seo_keywords',
    )
    
    readonly_fields = ('rating',)  # Rating field is read-only

    inlines = [ProductSizeInline]

    def get_form(self, request, obj=None, **kwargs):
        """
        Customize the form for products with sizes.
        Makes the stock field readonly if the product has sizes.
        """
        form = super().get_form(request, obj, **kwargs)
        if obj and obj.has_sizes:
            form.base_fields['stock'].widget.attrs['readonly'] = True
            form.base_fields['stock'].help_text = 'Stock is managed through product sizes'
        return form
    
    def get_sale_display(self, obj):
        """
        Display sale price with discount info, or "No sale" if not on sale.
        """
        sale_price = obj.get_sale_price
        if sale_price:
            return f"${sale_price} (${obj.base_price} - {obj.sale.discount_percentage}% off)"
        return "No sale"
    get_sale_display.short_description = 'Sale Price'

# Category admin configuration
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('friendly_name', 'name', 'seo_title', 'seo_meta_description')
    search_fields = ('name', 'friendly_name', 'seo_title', 'seo_meta_description')
    ordering = ('name',)
    fields = ('name', 'friendly_name', 'description', 'seo_title', 'seo_meta_description', 'seo_keywords')

# SubCategory admin configuration
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('friendly_name', 'name', 'category', 'seo_title', 'seo_meta_description')
    search_fields = ('name', 'friendly_name', 'seo_title', 'seo_meta_description')
    ordering = ('name',)
    list_filter = ('category',)
    fields = ('name', 'friendly_name', 'category', 'description', 'seo_title', 'seo_meta_description', 'seo_keywords')

# Register models with the admin site
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Sale)
