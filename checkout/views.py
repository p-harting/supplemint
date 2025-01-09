from django.shortcuts import (
    render, redirect, reverse, get_object_or_404, HttpResponse)
from django.views.decorators.http import require_POST
from referrals.models import ReferralTransaction
from django.contrib import messages
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from .forms import OrderForm
from .models import Order, OrderLineItem
from products.models import Product
from profiles.models import UserProfile
from profiles.forms import UserProfileForm
from bag.contexts import bag_contents
from bag.models import DiscountCode
import stripe
import json
from decimal import Decimal
from django.db.models import F


@require_POST
def cache_checkout_data(request):
    """
    Caches checkout data to Stripe's PaymentIntent metadata.
    Used to store the bag contents and user info before confirming the payment.
    """
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'bag': json.dumps(request.session.get('bag', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(
            request,
            'Sorry, your payment cannot be processed right now. '
            'Please try again later.')
        return HttpResponse(content=e, status=400)


def checkout(request):
    """
    Handles the checkout process:
    - Displays the checkout form.
    - Calculates the order total including any discounts.
    - Creates a Stripe PaymentIntent for payment processing.
    - Saves the order and order line items upon successful form submission.
    """
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    # Check if there are items in the bag
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "There's nothing in your bag at the moment.")
        return redirect(reverse('products'))

    current_bag = bag_contents(request)
    total = current_bag['grand_total']

    # Apply discount code if available
    discount_code = request.session.get('discount_code')
    if discount_code:
        try:
            code = DiscountCode.objects.get(code=discount_code, is_active=True)
            discount_amount = code.apply_discount(total)
            total -= discount_amount
            messages.success(
                request,
                f'Discount code {code.code} applied! '
                f'${discount_amount:.2f} off your order.')
        except DiscountCode.DoesNotExist:
            messages.error(request, 'Invalid discount code.')
            request.session.pop('discount_code', None)

    # Create Stripe payment intent
    stripe_total = round(total * 100)
    stripe.api_key = stripe_secret_key
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
    )

    # Handle form submission
    if request.method == 'POST':
        form_data = {
            'full_name': request.POST.get('full_name', ''),
            'email': request.POST.get('email', ''),
            'phone_number': request.POST.get('phone_number', ''),
            'country': request.POST.get('country', ''),
            'postcode': request.POST.get('postcode', ''),
            'town_or_city': request.POST.get('town_or_city', ''),
            'street_address1': request.POST.get('street_address1', ''),
            'street_address2': request.POST.get('street_address2', ''),
            'county': request.POST.get('county', ''),
        }

        # Pre-fill the form with their profile data
        if request.user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=request.user)
                profile_form = UserProfileForm(request.POST, instance=profile)
                if profile_form.is_valid():
                    profile_form.save()
                    if not form_data['full_name']:
                        form_data['full_name'] = (
                            f"{profile.user.first_name}"
                            f"{profile.user.last_name}")
                    if not form_data['email']:
                        form_data['email'] = profile.user.email
            except UserProfile.DoesNotExist:
                pass

        # Create the order form and validate it
        order_form = OrderForm(form_data, user=request.user)
        if order_form.is_valid():
            current_bag = bag_contents(request)
            total = current_bag['grand_total']

            order = order_form.save(commit=False)

            # Apply discount code if applicable
            discount_code = request.session.get('discount_code')
            if discount_code:
                try:
                    code = DiscountCode.objects.get(
                        code=discount_code, is_active=True)
                    order.discount_code = code
                    discount_amount = code.apply_discount(total)
                    order.discount_amount = discount_amount
                    total -= discount_amount
                except DiscountCode.DoesNotExist:
                    messages.error(
                        request, 'Invalid or inactive discount code.')
                    request.session.pop('discount_code', None)

            # Save the order and link the stripe payment ID
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid
            order.original_bag = json.dumps(bag)
            order.grand_total = total
            order.save()

            # Create order line items based on the bag contents
            for item_id, item_data in bag.items():
                try:
                    product = Product.objects.get(id=item_id)
                    if isinstance(item_data, int):
                        order_line_item = OrderLineItem(
                            order=order,
                            product=product,
                            quantity=item_data,
                        )
                        order_line_item.save()
                    else:
                        if 'items_by_size' in item_data:
                            for size, size_data in (
                                    item_data['items_by_size'].items()):
                                if isinstance(size_data, dict):
                                    quantity = size_data['quantity']
                                else:
                                    quantity = size_data
                                order_line_item = OrderLineItem(
                                    order=order,
                                    product=product,
                                    quantity=int(quantity),
                                    product_size=size,
                                )
                                order_line_item.save()
                        else:
                            # Handle items without sizes but with other data
                            order_line_item = OrderLineItem(
                                order=order,
                                product=product,
                                quantity=item_data,
                            )
                            order_line_item.save()
                except Product.DoesNotExist:
                    messages.error(
                        request,
                        "A product in your bag wasn't found."
                        "Please contact us.")
                    order.delete()
                    return redirect(reverse('view_bag'))

            # Update the order total
            order.update_total()
            request.session['save_info'] = 'save-info' in request.POST
            return redirect(
                reverse('checkout_success', args=[order.order_number]))
        else:
            messages.error(
                request,
                'There was an error with your form. '
                'Please check your details.')

    # Pre-fill the order form if the user is authenticated
    order = None
    if request.user.is_authenticated:
        try:
            profile = UserProfile.objects.get(user=request.user)
            order = Order(
                full_name=profile.full_name,
                email=profile.email,
                phone_number=profile.phone_number,
                street_address1=profile.street_address1,
                street_address2=profile.street_address2,
                town_or_city=profile.town_or_city,
                county=profile.county,
                postcode=profile.postcode,
                country=profile.country
            )
        except UserProfile.DoesNotExist:
            print("No profile found for user")

    order_form = OrderForm(instance=order)

    # Warn if Stripe public key is missing
    if not stripe_public_key:
        messages.warning(
            request,
            'Stripe public key is missing. '
            'Did you set it in your environment?')

    # Render the checkout page
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
        'discount_code': discount_code,
    }

    return render(request, template, context)


def checkout_success(request, order_number):
    """
    Handles the success page after the checkout process:
    - Assigns the order to the user's profile.
    - Creates a referral transaction if applicable.
    - Sends a confirmation email to the customer.
    - Clears the shopping bag and shows recommended products.
    """
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)

    # Assign the order to the user profile if authenticated
    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        order.user_profile = profile
        order.save()

        # Handle referral commission if the user was referred
        if profile.referred_by:
            commission_rate = Decimal('0.05')
            commission_amount = order.grand_total * commission_rate
            ReferralTransaction.objects.create(
                referrer=profile.referred_by,
                referred_user=request.user,
                order_number=order.order_number,
                amount=order.grand_total,
                commission=commission_amount
            )

        # Save the user's address information if requested
        if save_info:
            profile_data = {
                'default_phone_number': order.phone_number,
                'default_country': order.country,
                'default_postcode': order.postcode,
                'default_town_or_city': order.town_or_city,
                'default_street_address1': order.street_address1,
                'default_street_address2': order.street_address2,
                'default_county': order.county,
            }
            user_profile_form = UserProfileForm(profile_data, instance=profile)
            if user_profile_form.is_valid():
                user_profile_form.save()

    # Update discount code balance if applicable
    if order.discount_code:
        DiscountCode.objects.filter(id=order.discount_code.id).update(
            remaining_balance=F('remaining_balance') - order.discount_amount
        )

    # Send order confirmation email
    if 'email_sent' not in request.session:
        subject = f'Order Confirmation - {order.order_number}'
        html_body = render_to_string(
            'checkout/order_confirmation_email.html',
            {'order': order}
        )
        email = EmailMultiAlternatives(
            subject,
            html_body,
            settings.DEFAULT_FROM_EMAIL,
            [order.email]
        )
        email.content_subtype = "html"
        email.send()
        request.session['email_sent'] = True
        messages.success(
            request,
            f'Order successfully processed! '
            f'Your order number is {order_number}.'
            f'A confirmation email has been sent to {order.email}.')

    # Clear the shopping bag from the session
    if 'bag' in request.session:
        del request.session['bag']

    # Recommend products for the user
    available_products = Product.objects.filter(stock__gt=0)
    if available_products.count() >= 6:
        recommended_products = available_products.order_by('?')[:6]
    else:
        recommended_products = Product.objects.order_by('?')[:6]

    # Render the success page
    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'recommended_products': recommended_products,
    }

    return render(request, template, context)
