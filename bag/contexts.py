from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product


def bag_contents(request):
    """Calculate and return the shopping bag context data.

    This includes item details, total cost, product count, delivery cost,
    free delivery delta, and the grand total.
    """
    bag_items = []
    total = 0
    product_count = 0
    bag = request.session.get('bag', {})

    for item_id, item_data in bag.items():
        product = get_object_or_404(Product, pk=item_id)
        if isinstance(item_data, int):
            # Item without size selection
            price = Decimal(item_data['price'])
            original_price = Decimal(item_data['original_price'])
            total += item_data['quantity'] * price
            product_count += item_data['quantity']
            bag_items.append({
                'item_id': item_id,
                'quantity': item_data['quantity'],
                'product': product,
                'price': price,
                'original_price': original_price,
            })
        else:
            # Item with size selection
            if 'items_by_size' in item_data:
                for size, size_data in item_data['items_by_size'].items():
                    if isinstance(size_data, dict):
                        # New format with explicit price and quantity
                        quantity = size_data['quantity']
                        price = Decimal(size_data['price'])
                    else:
                        # Old format with just quantity
                        quantity = size_data
                        product_size = product.sizes.filter(name=size).first()
                        price = (product_size.price if product_size
                                 else product.base_price)
                    price = Decimal(size_data['price'])
                    original_price = Decimal(size_data['original_price'])
                    total += quantity * price
                    product_count += quantity
                    bag_items.append({
                        'item_id': item_id,
                        'quantity': quantity,
                        'product': product,
                        'size': size,
                        'price': price,
                        'original_price': original_price,
                    })
            else:
                # Handle items without sizes
                price = Decimal(item_data['price'])
                original_price = Decimal(item_data['original_price'])
                total += item_data['quantity'] * price
                product_count += item_data['quantity']
                bag_items.append({
                    'item_id': item_id,
                    'quantity': item_data['quantity'],
                    'product': product,
                    'price': price,
                    'original_price': original_price,
                })

    # Calculate delivery and free delivery delta
    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = 0
        free_delivery_delta = 0

    grand_total = delivery + total

    return {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }
