from django.contrib import admin
from .models import ReferralCode, ReferralTransaction

@admin.register(ReferralCode)
class ReferralCodeAdmin(admin.ModelAdmin):
    list_display = ('user', 'code', 'created_at', 'total_earnings')
    search_fields = ('user__username', 'code')
    readonly_fields = ('created_at',)

@admin.register(ReferralTransaction)
class ReferralTransactionAdmin(admin.ModelAdmin):
    list_display = ('referrer', 'referred_user', 'order_number', 'amount', 'commission', 'created_at')
    search_fields = ('referrer__username', 'referred_user__username', 'order_number')
    readonly_fields = ('created_at',)
