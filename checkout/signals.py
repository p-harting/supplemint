from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import OrderLineItem

@receiver(post_save, sender=OrderLineItem)
def update_on_save(sender, instance, created, **kwargs):
    """
    Update order total and product stock on lineitem update/create
    """
    if created:
        product = instance.product
        if instance.product_size:
            product_size = product.sizes.get(name=instance.product_size)
            product_size.stock -= instance.quantity
            product_size.save()
        else:
            product.stock -= instance.quantity
            product.save()
    instance.order.update_total()

@receiver(post_delete, sender=OrderLineItem)
def update_on_delete(sender, instance, **kwargs):
    """
    Update order total and restore product stock on lineitem delete
    """
    product = instance.product
    if instance.product_size:
        product_size = product.sizes.get(name=instance.product_size)
        product_size.stock += instance.quantity
        product_size.save()
    else:
        product.stock += instance.quantity
        product.save()
    instance.order.update_total()
