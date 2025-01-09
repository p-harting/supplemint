from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product
import random
from django.contrib import messages
from .models import NewsletterSubscriber, PageContent
from core.utils import validate_email
from django.core.exceptions import ValidationError


def index(request):
    """View for the homepage displaying random products."""
    # Retrieve all products from the database
    all_products = Product.objects.all()

    # If there are 4 or more products, pick 5 random products
    if len(all_products) >= 4:
        random_products = random.sample(list(all_products), 5)
    else:
        random_products = all_products  # If fewer than 4, show all products

    # Pass the random products to the template
    return render(
        request, 'home/index.html', {'random_products': random_products})


def shipping(request):
    """View for the Shipping Information page."""
    # Fetch the shipping page content
    page_content = get_object_or_404(PageContent, page='shipping')
    # Render the shipping page
    return render(
        request, 'home/shipping.html', {'page_content': page_content})


def returns(request):
    """View for the Returns Policy page."""
    # Fetch the returns page content
    page_content = get_object_or_404(PageContent, page='returns')
    return render(
        # Render the returns page
        request, 'home/returns.html', {'page_content': page_content})


def privacy(request):
    """View for the Privacy Policy page."""
    # Fetch the privacy page content
    page_content = get_object_or_404(PageContent, page='privacy')
    # Render the privacy page
    return render(
        request,
        'home/privacy.html', {'page_content': page_content})


def terms(request):
    """View for the Terms & Conditions page."""
    # Fetch the terms page content
    page_content = get_object_or_404(PageContent, page='terms')
    # Render the terms page
    return render(request, 'home/terms.html', {'page_content': page_content})


def custom_404(request, exception):
    """Custom 404 error page view."""
    # Render a custom 404 error page
    return render(request, '404.html', status=404)


def newsletter_subscribe(request):
    """View for subscribing to the newsletter."""
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            # Validate the email using the custom validation function
            validate_email(email)
            # If email is valid, save the subscriber
            NewsletterSubscriber.objects.create(email=email)
            messages.success(request, 'Thank you for subscribing!')
            return redirect('home')
        except ValidationError as e:
            # If email is invalid, display the error message
            messages.error(request, str(e))
    # Render the page with the form and any messages
    return render(request, 'home/index.html', {
        # Maintain existing context
        'random_products': Product.objects.all()[:5],
    })
