from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Admin configuration for the UserProfile model.

    Defines how UserProfile objects are displayed and managed in
    the admin interface.
    """
    list_display = (
        'user', 'referred_by', 'full_name', 'email', 'town_or_city', 'country')
    search_fields = (
        'user__username', 'referred_by__username', 'full_name', 'email')
    list_filter = ('referred_by', 'country')
    raw_id_fields = ('user', 'referred_by')
