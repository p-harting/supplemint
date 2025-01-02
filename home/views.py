from django.shortcuts import render
from products.models import Product
import random
from django.shortcuts import redirect
from django.contrib import messages
from .models import NewsletterSubscriber

def index(request):
    all_products = Product.objects.all()

    if len(all_products) >= 4:
        random_products = random.sample(list(all_products), 6)
    else:
        random_products = all_products

    return render(request, 'home/index.html', {'random_products': random_products})

from django.shortcuts import get_object_or_404
from .models import PageContent

def shipping(request):
    page_content = get_object_or_404(PageContent, page='shipping')
    return render(request, 'home/shipping.html', {'page_content': page_content})

def returns(request):
    page_content = get_object_or_404(PageContent, page='returns')
    return render(request, 'home/returns.html', {'page_content': page_content})

def privacy(request):
    page_content = get_object_or_404(PageContent, page='privacy')
    return render(request, 'home/privacy.html', {'page_content': page_content})

def terms(request):
    page_content = get_object_or_404(PageContent, page='terms')
    return render(request, 'home/terms.html', {'page_content': page_content})

def custom_404(request, exception):
    return render(request, '404.html', status=404)

def newsletter_subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            try:
                NewsletterSubscriber.objects.create(email=email)
                messages.success(request, 'Thank you for subscribing!')
            except:
                messages.error(request, 'This email is already subscribed.')
        else:
            messages.error(request, 'Please enter a valid email address.')
    return redirect('home')
