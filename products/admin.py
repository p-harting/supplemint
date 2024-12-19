from django.contrib import admin
from .models import Product, Category, SubCategory, ProductSize

class ProductSizeInline(admin.TabularInline):
    model = ProductSize
    extra = 1
    fields = ('name', 'price')

class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'sku',
        'name',
        'category',
        'subcategory',
        'base_price',  # Changed from 'price'
        'rating',
        'image',
    )
    ordering = ('sku',)

    fields = (
        'sku',
        'name',
        'category',
        'subcategory',
        'description',
        'detailed_description',
        'nutritional_info',
        'how_to_use',
        'key_facts',
        'has_sizes',
        'base_price',  # Changed from 'price'
        'rating',
        'image',
        'slug',
    )
    
    inlines = [ProductSizeInline]  # Add this line to include the size editor

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj and obj.has_sizes:
            form.base_fields['base_price'].help_text = 'This is the default price if no size is selected'
        return form

# CategoryAdmin and SubCategoryAdmin remain unchanged
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
        'seo_title',
        'seo_meta_description',
    )
    search_fields = ('name', 'friendly_name', 'seo_title', 'seo_meta_description')
    ordering = ('name',)

    fields = (
        'name',
        'friendly_name',
        'description',
        'seo_title',
        'seo_meta_description',
        'seo_keywords',
    )


class SubCategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
        'category',
        'seo_title',
        'seo_meta_description',
    )
    search_fields = ('name', 'friendly_name', 'seo_title', 'seo_meta_description')
    ordering = ('name',)
    list_filter = ('category',)

    fields = (
        'name',
        'friendly_name',
        'category',
        'description',
        'seo_title',
        'seo_meta_description',
        'seo_keywords',
    )

# Register your models
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)