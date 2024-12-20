from django.contrib import admin
from .models import Product, Category, SubCategory, ProductSize, Sale

class ProductSizeInline(admin.TabularInline):
    model = ProductSize
    extra = 1
    fields = ('name', 'price', 'stock')

class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'sku',
        'name',
        'category',
        'subcategory',
        'base_price',
        'get_sale_display',
        'get_stock_display',
        'rating',
        'image',
    )
    
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
        'base_price',
        'sale',
        'stock',
        'rating',
        'image',
        'slug',
    )

    
    inlines = [ProductSizeInline]

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj and obj.has_sizes:
            form.base_fields['stock'].widget.attrs['readonly'] = True
            form.base_fields['stock'].help_text = 'Stock is managed through product sizes'
        return form
    
    def get_sale_display(self, obj):
        sale_price = obj.get_sale_price
        if sale_price is not None:
            return f"${sale_price} (${obj.base_price} - {obj.sale.discount_percentage}% off)"
        return "No sale"
    get_sale_display.short_description = 'Sale Price'

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

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Sale)