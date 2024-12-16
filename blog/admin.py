from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'is_published')
    list_filter = ('is_published', 'created_at', 'author')
    search_fields = ('title', 'content', 'meta_description', 'meta_keywords')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Post Content', {
            'fields': ('title', 'slug', 'author', 'content', 'featured_image')
        }),
        ('SEO Settings', {
            'fields': ('meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
        ('Publishing', {
            'fields': ('is_published', 'created_at', 'updated_at')
        }),
    )