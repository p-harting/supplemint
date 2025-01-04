from django.contrib import admin
from .models import ContactMessage

class ContactMessageAdmin(admin.ModelAdmin):
    """Admin configuration for the ContactMessage model.

    Defines how ContactMessage objects are displayed and managed in the admin interface.
    """
    # Display these fields in the list view of the admin interface
    list_display = ('name', 'email', 'subject', 'created_at')
    
    # Enable search functionality for these fields in the admin interface
    search_fields = ('name', 'email', 'subject')
    
    # Add filters to the admin interface for easy filtering by creation date
    list_filter = ('created_at',)
    
    # Order the messages by creation date, with the newest messages first
    ordering = ('-created_at',)

# Register the ContactMessage model with the custom admin configuration
admin.site.register(ContactMessage, ContactMessageAdmin)
