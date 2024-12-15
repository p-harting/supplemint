from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'referred_by', 'default_phone_number', 'default_town_or_city', 'country')
    search_fields = ('user__username', 'referred_by__username', 'default_phone_number')
    list_filter = ('referred_by',)
    raw_id_fields = ('user', 'referred_by')
