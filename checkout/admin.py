from django.contrib import admin
from .models import Order, OrderLineItem


# Inline display for order line items within the order admin
class OrderLineItemAdminInline(admin.TabularInline):
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)  # Display line item total as read-only


# Admin configuration for the Order model
class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderLineItemAdminInline,)  # Include line items in the order admin

    readonly_fields = ('order_number', 'date',  # Make certain fields read-only
                       'delivery_cost', 'order_total',
                       'grand_total', 'original_bag', 'stripe_pid',)

    fields = ('order_number', 'date', 'full_name',  # Fields to display in the order form
              'email', 'phone_number', 'country',
              'postcode', 'town_or_city', 'street_address1',
              'street_address2', 'county', 'delivery_cost',
              'order_total', 'grand_total', 'original_bag', 'stripe_pid',)

    list_display = ('order_number', 'date', 'full_name',  # Columns to show in the list view
                    'order_total', 'delivery_cost',
                    'grand_total',)

    ordering = ('-date',)  # Order by date descending

# Register the Order model with the admin site
admin.site.register(Order, OrderAdmin)
