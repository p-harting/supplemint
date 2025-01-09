from django.contrib import admin
from .models import ReferralCode, ReferralTransaction


@admin.register(ReferralCode)
class ReferralCodeAdmin(admin.ModelAdmin):
    # Configure fields displayed in the admin list and detail views
    list_display = ('user', 'code', 'created_at', 'total_earnings',
                    'unredeemed_balance')
    search_fields = ('user__username', 'code')
    readonly_fields = ('created_at',)
    fields = (
        'user', 'code', 'total_earnings', 'unredeemed_balance',
        'created_at')


@admin.register(ReferralTransaction)
class ReferralTransactionAdmin(admin.ModelAdmin):
    # Configure fields displayed in the admin list and detail views
    list_display = ('referrer', 'referred_user', 'order_number', 'amount',
                    'commission', 'created_at')
    search_fields = ('referrer__username', 'referred_user__username',
                     'order_number')
    readonly_fields = ('created_at',)
