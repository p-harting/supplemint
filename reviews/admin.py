from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    # Display fields in the admin list view
    list_display = ('user', 'product', 'rating', 'created_at', 'approved')

    # Filter reviews by approval status, rating, and creation date
    list_filter = ('approved', 'rating', 'created_at')

    # Enable search by user username, product name, and review text
    search_fields = ('user__username', 'product__name', 'text')

    # Add custom action to approve selected reviews
    actions = ['approve_reviews']

    def approve_reviews(self, request, queryset):
        """
        Approves selected reviews by setting 'approved' to True.
        """
        queryset.update(approved=True)

    # Short description for the custom action
    approve_reviews.short_description = "Approve selected reviews"
