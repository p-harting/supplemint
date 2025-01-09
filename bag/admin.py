from django.contrib import admin
from .models import DiscountCode


@admin.register(DiscountCode)
class DiscountCodeAdmin(admin.ModelAdmin):
    """Admin configuration for the DiscountCode model.

    Defines how DiscountCode objects are displayed and managed
    in the admin interface.
    """
    list_display = ('code', 'amount', 'remaining_balance', 'is_active',
                    'created_at')
    # Filters for status and creation date
    list_filter = ('is_active', 'created_at')
    # Enable search by code
    search_fields = ('code',)
    # Fields that cannot be edited
    readonly_fields = ('remaining_balance', 'created_at', 'updated_at')
    # Default order by newest created first
    ordering = ('-created_at',)
