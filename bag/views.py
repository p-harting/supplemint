from django.shortcuts import (
    render, redirect, reverse, HttpResponse, get_object_or_404
)
from django.contrib import messages
from products.models import Product
from .models import DiscountCode


def view_bag(request):
    """ A view that renders the bag contents page """

    return render(request, 'bag/bag.html')

from django.http import JsonResponse
from bag.contexts import bag_contents

def apply_discount(request):
    """ Apply discount code to the session """
    if request.method == 'POST':
        code = request.POST.get('discount_code')
        try:
            discount_code = DiscountCode.objects.get(code=code, is_active=True)
            if discount_code.remaining_balance > 0:
                request.session['discount_code'] = code
                # Calculate new total
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
    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    size = None
    bag = request.session.get('bag', {})
    
    if 'product_size' in request.POST:
        size = request.POST['product_size']
        product_size = product.sizes.filter(name=size).first()
        
        if not product_size:
            messages.error(request, "Selected size not found")
            return redirect(redirect_url)
            
        if quantity > product_size.stock:
            messages.error(request, f"Sorry, only {product_size.stock} items available in size {size}")
            return redirect(redirect_url)
    else:
        if quantity > product.stock:
            messages.error(request, f"Sorry, only {product.stock} items available")
            return redirect(redirect_url)

    if size:
        product_size = product.sizes.filter(name=size).first()
        if product_size:
            size_price = product_size.price
        else:
            size_price = product.base_price

        if item_id in bag:
            if isinstance(bag[item_id], dict):
                if size in bag[item_id]['items_by_size']:
                    bag[item_id]['items_by_size'][size]['quantity'] += quantity
                    messages.success(request,
                                    (f'Updated size {size.upper()} '
                                     f'{product.name} quantity to '
                                     f'{bag[item_id]["items_by_size"][size]["quantity"]}'))
                else:
                    bag[item_id]['items_by_size'][size] = {
                        'quantity': quantity,
                        'price': str(size_price)
                    }
                    messages.success(request,
                                    (f'Added size {size.upper()} '
                                     f'{product.name} to your bag'))
            else:
                bag[item_id] = {
                    'items_by_size': {
                        size: {
                            'quantity': quantity,
                            'price': str(size_price)
                        }
                    }
                }
        else:
            bag[item_id] = {
                'items_by_size': {
                    size: {
                        'quantity': quantity,
                        'price': str(size_price)
                    }
                }
            }
    else:
        if item_id in bag:
            bag[item_id] += quantity
            messages.success(request, f'Updated {product.name} quantity to {bag[item_id]}')
        else:
            bag[item_id] = quantity
            messages.success(request, f'Added {product.name} to your bag')

    request.session['bag'] = bag
    return redirect(redirect_url)

def adjust_bag(request, item_id):
    """Adjust the quantity of the specified product to the specified amount"""

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    bag = request.session.get('bag', {})

    if size:
        if quantity > 0:
            bag[item_id]['items_by_size'][size] = quantity
            messages.success(request,
                             (f'Updated size {size.upper()} '
                              f'{product.name} quantity to '
                              f'{bag[item_id]["items_by_size"][size]}'))
        else:
            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
            messages.success(request,
                             (f'Removed size {size.upper()} '
                              f'{product.name} from your bag'))
    else:
        if quantity > 0:
            bag[item_id] = quantity
            messages.success(request,
                             (f'Updated {product.name} '
                              f'quantity to {bag[item_id]}'))
        else:
            bag.pop(item_id)
            messages.success(request,
                             (f'Removed {product.name} '
                              f'from your bag'))

    request.session['bag'] = bag
    return redirect(reverse('view_bag'))


def remove_from_bag(request, item_id):
    """Remove the item from the shopping bag"""

    try:
        product = get_object_or_404(Product, pk=item_id)
        size = None
        if 'product_size' in request.POST:
            size = request.POST['product_size']
        bag = request.session.get('bag', {})

        if size:
            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
            messages.success(request,
                             (f'Removed size {size.upper()} '
                              f'{product.name} from your bag'))
        else:
            bag.pop(item_id)
            messages.success(request, f'Removed {product.name} from your bag')

        request.session['bag'] = bag
        return redirect(reverse('view_bag'))

    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return redirect(reverse('view_bag'))
