from django.contrib import admin
from .models import DiscountCode

@admin.register(DiscountCode)
class DiscountCodeAdmin(admin.ModelAdmin):
    """Admin configuration for the DiscountCode model.

    Defines how DiscountCode objects are displayed and managed in the admin interface.
    """
    list_display = ('code', 'amount', 'remaining_balance', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')  # Filters for status and creation date
    search_fields = ('code',)  # Enable search by code
    readonly_fields = ('remaining_balance', 'created_at', 'updated_at')  # Fields that cannot be edited
    ordering = ('-created_at',)  # Default order by newest created first
