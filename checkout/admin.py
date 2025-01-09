from django.contrib import admin
from .models import Order, OrderLineItem


# Inline display for order line items within the order admin
class OrderLineItemAdminInline(admin.TabularInline):
    model = OrderLineItem
    # Display line item total as read-only
    readonly_fields = ('lineitem_total',)


# Admin configuration for the Order model
class OrderAdmin(admin.ModelAdmin):
    # Include line items in the order admin
    inlines = (OrderLineItemAdminInline,)
    # Make certain fields read-only
    readonly_fields = ('order_number', 'date',
                       'delivery_cost', 'order_total',
                       'grand_total', 'original_bag', 'stripe_pid',)
    # Fields to display in the order form
    fields = ('order_number', 'date', 'full_name',
              'email', 'phone_number', 'country',
              'postcode', 'town_or_city', 'street_address1',
              'street_address2', 'county', 'delivery_cost',
              'order_total', 'grand_total', 'original_bag', 'stripe_pid',)
    # Columns to show in the list view
    list_display = ('order_number', 'date', 'full_name',
                    'order_total', 'delivery_cost',
                    'grand_total',)

    ordering = ('-date',)  # Order by date descending


# Register the Order model with the admin site
admin.site.register(Order, OrderAdmin)
