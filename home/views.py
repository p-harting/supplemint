from django.shortcuts import render
from products.models import Product
import random
from django.shortcuts import redirect
from django.contrib import messages
from .models import NewsletterSubscriber, PageContent
from django.shortcuts import get_object_or_404

def index(request):
    """View for the homepage displaying random products."""
    
    all_products = Product.objects.all()  # Retrieve all products from the database

    # If there are 4 or more products, pick 5 random products
    if len(all_products) >= 4:
        random_products = random.sample(list(all_products), 5)
    else:
        random_products = all_products  # If fewer than 4, show all products

    return render(request, 'home/index.html', {'random_products': random_products})  # Pass the random products to the template

def shipping(request):
    """View for the Shipping Information page."""
    
    page_content = get_object_or_404(PageContent, page='shipping')  # Fetch the shipping page content
    return render(request, 'home/shipping.html', {'page_content': page_content})  # Render the shipping page

def returns(request):
    """View for the Returns Policy page."""
    
    page_content = get_object_or_404(PageContent, page='returns')  # Fetch the returns page content
    return render(request, 'home/returns.html', {'page_content': page_content})  # Render the returns page

def privacy(request):
    """View for the Privacy Policy page."""
    
    page_content = get_object_or_404(PageContent, page='privacy')  # Fetch the privacy page content
    return render(request, 'home/privacy.html', {'page_content': page_content})  # Render the privacy page

def terms(request):
    """View for the Terms & Conditions page."""
    
    page_content = get_object_or_404(PageContent, page='terms')  # Fetch the terms page content
    return render(request, 'home/terms.html', {'page_content': page_content})  # Render the terms page

def custom_404(request, exception):
    """Custom 404 error page view."""
    
    return render(request, '404.html', status=404)  # Render a custom 404 error page

def newsletter_subscribe(request):
    """View for subscribing to the newsletter."""
    
    if request.method == 'POST':  # If the request is a POST request
        email = request.POST.get('email')  # Get the email from the form input
        if email:
            try:
                NewsletterSubscriber.objects.create(email=email)  # Create a new subscription entry
                messages.success(request, 'Thank you for subscribing!')  # Success message
            except:
                messages.error(request, 'This email is already subscribed.')  # Error if email is already subscribed
        else:
            messages.error(request, 'Please enter a valid email address.')  # Error if email is not provided
    return redirect('home')  # Redirect to the homepage after submission
