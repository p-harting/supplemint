from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Admin configuration for the UserProfile model.

    Defines how UserProfile objects are displayed and managed in the admin interface.
    """
    # Display these fields in the list view of the admin interface
    list_display = ('user', 'referred_by', 'full_name', 'email', 'town_or_city', 'country')
    
    # Enable search functionality for these fields in the admin interface
    search_fields = ('user__username', 'referred_by__username', 'full_name', 'email')
    
    # Add filters to the admin interface for easy filtering by referral and country
    list_filter = ('referred_by', 'country')
    
    # Use raw ID fields for 'user' and 'referred_by' to improve performance in large datasets
    raw_id_fields = ('user', 'referred_by')
