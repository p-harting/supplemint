from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import OrderLineItem


@receiver(post_save, sender=OrderLineItem)
def update_on_save(sender, instance, created, **kwargs):
    """
    Signal to update order total and product stock when
    a line item is created or updated.
    - If the line item is newly created, update the stock
    for the product or product size.
    - Always update the order's total after any change to the line item.
    """
    if created:
        product = instance.product
        # Check if the product has a size and update stock accordingly
        if instance.product_size:
            product_size = product.sizes.get(name=instance.product_size)
            # Decrease stock for the specific size
            product_size.stock -= instance.quantity
            product_size.save()
        else:
            # Decrease stock for the product itself
            product.stock -= instance.quantity
            product.save()
    # Update the total of the associated order after the line item change
    instance.order.update_total()


@receiver(post_delete, sender=OrderLineItem)
def update_on_delete(sender, instance, **kwargs):
    """
    Signal to update order total and
    restore product stock when a line item is deleted.
    - Restore the stock for the product or product size that was removed.
    - Always update the order's total after the line item is deleted.
    """
    product = instance.product
    # Check if the product has a size and restore stock accordingly
    if instance.product_size:
        product_size = product.sizes.get(name=instance.product_size)
        # Restore stock for the specific size
        product_size.stock += instance.quantity
        product_size.save()
    else:
        # Restore stock for the product itself
        product.stock += instance.quantity
        product.save()
    # Update the total of the associated order after the line item deletion
    instance.order.update_total()
