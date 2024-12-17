from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category, SubCategory
from django.db.models.functions import Lower
import random

def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all()
    query = None
    categories = None
    subcategories = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            if sortkey == 'category':
                sortkey = 'category__name'

            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)

        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if 'subcategory' in request.GET:
            subcategories = request.GET['subcategory'].split(',')
            products = products.filter(subcategory__name__in=subcategories)
            subcategories = SubCategory.objects.filter(name__in=subcategories)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))
            
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_subcategories': subcategories,
        'current_sorting': current_sorting,
    }

    return render(request, 'products/products.html', context)

def category_products(request, category_name):
    category = get_object_or_404(Category, name=category_name)
    products = Product.objects.filter(category=category)
    
    context = {
        'category': category,
        'products': products,
    }
    return render(request, 'products/products.html', context)

def subcategory_products(request, category_name, subcategory_name):
    category = get_object_or_404(Category, name=category_name)
    subcategory = get_object_or_404(SubCategory, name=subcategory_name, category=category)
    products = Product.objects.filter(subcategory=subcategory)
    
    context = {
        'category': category,
        'subcategory': subcategory,
        'products': products,
    }
    return render(request, 'products/products.html', context)

def product_detail(request, category_name, product_slug, subcategory_name=None):
    if subcategory_name:
        product = get_object_or_404(
            Product,
            slug=product_slug,
            category__name=category_name,
            subcategory__name=subcategory_name
        )
    else:
        product = get_object_or_404(
            Product,
            slug=product_slug,
            category__name=category_name,
        )
    
    category_products = Product.objects.filter(
        category__name=category_name
    ).exclude(id=product.id)
    
    if category_products.count() < 3:
        other_products = Product.objects.exclude(
            Q(id=product.id) | Q(category__name=category_name)
        )
        all_products = list(category_products) + list(other_products)
        random_products = random.sample(all_products, min(3, len(all_products)))
    else:
        random_products = random.sample(list(category_products), min(3, category_products.count()))

    context = {
        'product': product,
        'random_products': random_products,
    }
    return render(request, 'products/product_detail.html', context)