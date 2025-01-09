from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Admin configuration for the Post model.

    Defines how Post objects are displayed and managed in the admin interface.
    """
    # Display fields in the list view
    list_display = ('title', 'author', 'created_at', 'is_published')

    # Filters for status, creation date, and author
    list_filter = ('is_published', 'created_at', 'author')

    # Enable search by title, content, meta description, and meta keywords
    search_fields = ('title', 'content', 'meta_description', 'meta_keywords')

    # Automatically generate slug from title
    prepopulated_fields = {'slug': ('title',)}

    # Fields that cannot be edited in the admin
    readonly_fields = ('created_at', 'updated_at')

    # Organize fields into sections for clarity in the form view
    fieldsets = (
        ('Post Content', {
            'fields': ('title', 'slug', 'author', 'content', 'featured_image')
        }),
        ('SEO Settings', {
            'fields': ('meta_description', 'meta_keywords'),
            'classes': ('collapse',)  # Collapsible section for SEO fields
        }),
        ('Publishing', {
            'fields': ('is_published', 'created_at', 'updated_at')
        }),
    )
