from django.shortcuts import render
from products.models import Product
import random

def index(request):
    all_products = Product.objects.all()

    if len(all_products) >= 4:
        random_products = random.sample(list(all_products), 6)
    else:
        random_products = all_products

    return render(request, 'home/index.html', {'random_products': random_products})

def custom_404(request, exception):
    return render(request, '404.html', status=404)
