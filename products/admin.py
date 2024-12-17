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
        'detailed_description',
        'nutritional_info',
        'how_to_use',
        'key_facts',
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
    )


class SubCategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
        'category',
    )


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
