import uuid
from django.db import models
from django.db.models import Sum
from django.conf import settings
from products.models import Product
from profiles.models import UserProfile

class Order(models.Model):
    # Basic order details
    order_number = models.CharField(max_length=32, null=False, editable=False)  # Unique order number
    user_profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')  # User profile link
    full_name = models.CharField(max_length=50, null=False, blank=False)  # Customer's full name
    email = models.EmailField(max_length=254, null=False, blank=False)  # Customer's email
    phone_number = models.CharField(max_length=20, null=False, blank=False)  # Customer's phone number
    country = models.CharField(max_length=40, null=False, blank=False)  # Customer's country
    postcode = models.CharField(max_length=20, null=True, blank=True)  # Customer's postcode
    town_or_city = models.CharField(max_length=40, null=False, blank=False)  # Customer's town/city
    street_address1 = models.CharField(max_length=80, null=False, blank=False)  # Street address line 1
    street_address2 = models.CharField(max_length=80, null=True, blank=True)  # Street address line 2
    county = models.CharField(max_length=80, null=True, blank=True)  # Customer's county
    date = models.DateTimeField(auto_now_add=True)  # Order creation date
    delivery_cost = models.DecimalField(max_digits=6, decimal_places=2, null=False, default=0)  # Delivery cost
    order_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)  # Total order cost
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)  # Final total (including delivery & discount)
    original_bag = models.TextField(null=False, blank=False, default='')  # JSON-like string of the original shopping bag
    stripe_pid = models.CharField(max_length=254, null=False, blank=False, default='')  # Stripe payment ID
    discount_code = models.ForeignKey('bag.DiscountCode', on_delete=models.SET_NULL, null=True, blank=True)  # Discount code if applied
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)  # Discount amount

    def _generate_order_number(self):
        """
        Generate a random, unique order number using UUID.
        """
        return uuid.uuid4().hex.upper()

    def update_total(self):
        """
        Update grand total whenever a line item is added or updated.
        Takes into account delivery costs and discounts.
        """
        # Calculate order total from line items
        self.order_total = self.lineitems.aggregate(Sum('lineitem_total'))['lineitem_total__sum'] or 0
        
        # Calculate delivery cost based on threshold
        if self.order_total < settings.FREE_DELIVERY_THRESHOLD:
            self.delivery_cost = self.order_total * settings.STANDARD_DELIVERY_PERCENTAGE / 100
        else:
            self.delivery_cost = 0
        
        # Calculate grand total (order total + delivery cost - discount)
        total = self.order_total + self.delivery_cost
        if self.discount_amount:
            total -= self.discount_amount
        self.grand_total = total
        self.save()

    def save(self, *args, **kwargs):
        """
        Override the save method to set the order number if it hasn't been set.
        """
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        """
        String representation of the order.
        """
        return self.order_number


class OrderLineItem(models.Model):
    # Linking order with products
    order = models.ForeignKey(Order, null=False, blank=False, on_delete=models.CASCADE, related_name='lineitems')  # Order the item belongs to
    product = models.ForeignKey(Product, null=False, blank=False, on_delete=models.CASCADE)  # Product in the line item
    product_size = models.CharField(max_length=32, null=True, blank=True)  # Size of the product (if applicable)
    quantity = models.IntegerField(null=False, blank=False, default=0)  # Quantity of the product
    lineitem_total = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False, editable=False)  # Total price for this line item

    def save(self, *args, **kwargs):
        """
        Override the save method to calculate line item total 
        and update the order total.
        """
        # Calculate the total for this line item (price * quantity)
        self.lineitem_total = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        """
        String representation of the order line item.
        """
        return f'SKU {self.product.sku} on order {self.order.order_number}'
