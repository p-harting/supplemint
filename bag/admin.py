from django.contrib import admin
from .models import DiscountCode

@admin.register(DiscountCode)
class DiscountCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'amount', 'remaining_balance', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('code',)
    readonly_fields = ('remaining_balance', 'created_at', 'updated_at')
    ordering = ('-created_at',)
