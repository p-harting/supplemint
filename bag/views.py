from django.shortcuts import (
    render, redirect, reverse, HttpResponse, get_object_or_404
)
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from products.models import Product
from .models import DiscountCode
from bag.contexts import bag_contents


def view_bag(request):
    """Render the bag contents page."""
    return render(request, 'bag/bag.html')


def apply_discount(request):
    """Apply a discount code to the session and calculate the new total."""
    if request.method == 'POST':
        code = request.POST.get('discount_code')
        try:
            discount_code = DiscountCode.objects.get(code=code, is_active=True)
            if discount_code.remaining_balance > 0:
                request.session['discount_code'] = code
                current_bag = bag_contents(request)
                total = current_bag['grand_total']
                discount_amount = discount_code.apply_discount(total)
                new_total = total - discount_amount
                
                return JsonResponse({
                    'success': True,
                    'message': f'Discount code {code} applied! ${discount_amount:.2f} off your order.',
                    'new_total': f'{new_total:.2f}'
                })
            else:
                request.session.pop('discount_code', None)
                return JsonResponse({
                    'success': False,
                    'message': 'This discount code has no remaining balance'
                })
        except DiscountCode.DoesNotExist:
            request.session.pop('discount_code', None)
            return JsonResponse({
                'success': False,
                'message': 'Invalid discount code'
            })
    
    return JsonResponse({
        'success': False,
        'message': 'Invalid request method'
    })


def add_to_bag(request, item_id):
    """Add a product to the shopping bag with optional size and quantity."""
    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    size = request.POST.get('product_size') if 'product_size' in request.POST else None
    bag = request.session.get('bag', {})

    if size:
        product_size = product.sizes.filter(name=size).first()
        if not product_size:
            messages.error(request, "Selected size not found")
            return redirect(redirect_url)
            
        existing_quantity = 0
        if item_id in bag and isinstance(bag[item_id], dict) and 'items_by_size' in bag[item_id]:
            if size in bag[item_id]['items_by_size']:
                existing_quantity = bag[item_id]['items_by_size'][size]['quantity']
                
        total_quantity = existing_quantity + quantity
        if total_quantity > 99:
            messages.error(request, f"You can't have more than 99 items of the same product. You already have {existing_quantity} in your bag.")
            return redirect(redirect_url)
        if total_quantity > product_size.stock:
            messages.error(request, f"Only {product_size.stock} items available in size {size}. You already have {existing_quantity} in your bag.")
            return redirect(redirect_url)
        size_price = product_size.price if product_size else product.base_price
        # Calculate sale price based on size price if product is on sale
        if product.sale and product.sale.active:
            now = timezone.now()
            if product.sale.start_date <= now <= product.sale.end_date:
                discount = size_price * (product.sale.discount_percentage / 100)
                sale_price = round(size_price - discount, 2)
            else:
                sale_price = size_price
        else:
            sale_price = size_price

        if item_id in bag:
            bag[item_id].setdefault('items_by_size', {})
            if size in bag[item_id]['items_by_size']:
                bag[item_id]['items_by_size'][size]['quantity'] += quantity
                messages.success(request, f'Updated size {size.upper()} {product.name} quantity.')
            else:
                bag[item_id]['items_by_size'][size] = {
                    'quantity': quantity,
                    'price': str(sale_price),
                    'original_price': str(size_price)
                }
                messages.success(request, f'Added size {size.upper()} {product.name} to your bag.')
        else:
            bag[item_id] = {'items_by_size': {
                size: {
                    'quantity': quantity,
                    'price': str(sale_price),
                    'original_price': str(size_price)
                }
            }}
    else:
        existing_quantity = bag.get(item_id, 0)
        total_quantity = existing_quantity + quantity
        if total_quantity > 99:
            messages.error(request, f"You can't have more than 99 items of the same product. You already have {existing_quantity} in your bag.")
            return redirect(redirect_url)
        if total_quantity > product.stock:
            messages.error(request, f"Only {product.stock} items available. You already have {existing_quantity} in your bag.")
            return redirect(redirect_url)
        # Use the product's built-in sale price calculation
        sale_price = product.get_sale_price or product.base_price
        bag[item_id] = {
            'quantity': bag.get(item_id, {}).get('quantity', 0) + quantity,
            'price': str(sale_price),
            'original_price': str(product.base_price)
        }
        messages.success(request, f'Updated {product.name} quantity to {bag[item_id]["quantity"]}.')

    request.session['bag'] = bag
    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """Adjust the quantity of a product or size in the shopping bag."""
    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    size = request.POST.get('product_size') if 'product_size' in request.POST else None
    bag = request.session.get('bag', {})

    if size:
        if item_id in bag and isinstance(bag[item_id], dict) and 'items_by_size' in bag[item_id]:
            if size in bag[item_id]['items_by_size']:
                existing_price = bag[item_id]['items_by_size'][size]['price']
                product_size = product.sizes.filter(name=size).first()
                
                if not product_size:
                    messages.error(request, "Selected size is no longer available")
                    return redirect(reverse('view_bag'))
                    
                if quantity > 99:
                    messages.error(request, "You can't have more than 99 items of the same product")
                    return redirect(reverse('view_bag'))
                    
                if quantity > product_size.stock:
                    existing_quantity = bag[item_id]['items_by_size'][size]['quantity']
                    messages.error(request, f"Only {product_size.stock} items available in size {size}. You already have {existing_quantity} in your bag.")
                    return redirect(reverse('view_bag'))
                    
                if quantity > 0:
                    bag[item_id]['items_by_size'][size] = {'quantity': quantity, 'price': existing_price}
                    messages.success(request, f'Updated size {size.upper()} {product.name} quantity to {quantity}.')
                else:
                    del bag[item_id]['items_by_size'][size]
                    if not bag[item_id]['items_by_size']:
                        bag.pop(item_id)
                    messages.success(request, f'Removed size {size.upper()} {product.name} from your bag.')
            else:
                messages.error(request, "Size not found in your bag.")
        else:
            messages.error(request, "Item not found in your bag.")
    else:
        # Handle non-size items
        if item_id in bag and isinstance(bag[item_id], int):
            if quantity > 99:
                messages.error(request, "You can't have more than 99 items of the same product")
                return redirect(reverse('view_bag'))
                
            if quantity > product.stock:
                existing_quantity = bag[item_id]
                messages.error(request, f"Only {product.stock} items available. You already have {existing_quantity} in your bag.")
                return redirect(reverse('view_bag'))
                
            if quantity > 0:
                bag[item_id] = quantity
                messages.success(request, f'Updated {product.name} quantity to {bag[item_id]}.')
            else:
                bag.pop(item_id)
                messages.success(request, f'Removed {product.name} from your bag.')
        else:
            messages.error(request, "Item not found in the bag.")

    request.session['bag'] = bag
    return redirect(reverse('view_bag'))

def remove_from_bag(request, item_id):
    """Remove a product or size from the shopping bag."""
    try:
        product = get_object_or_404(Product, pk=item_id)
        size = request.POST.get('product_size') if 'product_size' in request.POST else None
        bag = request.session.get('bag', {})

        if size:
            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
            messages.success(request, f'Removed size {size.upper()} {product.name} from your bag.')
        else:
            bag.pop(item_id)
            messages.success(request, f'Removed {product.name} from your bag.')

        request.session['bag'] = bag
        return redirect(reverse('view_bag'))
    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return redirect(reverse('view_bag'))
