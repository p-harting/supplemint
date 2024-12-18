from django.contrib import admin
from .models import Product, Category, SubCategory

class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'sku',
        'name',
        'category',
        'subcategory',
        'price',
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
        'price',
        'rating',
        'image',
        'slug',
    )


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
    )
    search_fields = ('name', 'friendly_name')
    ordering = ('name',)
    list_filter = ('category',)

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
