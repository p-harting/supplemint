from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category, SubCategory
from django.db.models.functions import Lower
from django.core.paginator import Paginator
import random
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import ProductForm

@login_required
@user_passes_test(lambda u: u.is_superuser)
def product_management(request):
    """ View to manage all products in the admin panel """
    products = Product.objects.all()
    return render(request, 'products/product_management.html', {
        'products': products
    })

@login_required
@user_passes_test(lambda u: u.is_superuser)
def add_product(request):
    """ View to add a new product to the database """
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully!')
            return redirect('product_management')
    else:
        form = ProductForm()
    return render(request, 'products/product_form.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def edit_product(request, product_id):
    """ View to edit an existing product """
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('product_management')
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/product_form.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_product(request, product_id):
    """ View to delete a product from the database """
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully!')
    return redirect('product_management')

def all_products(request):
    """ View to display all products with sorting and search functionality """
    products = Product.objects.all()
    query = None
    categories = None
    subcategories = None
    sort = None
    direction = None

    if request.GET:
        # Sorting
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            if sortkey == 'category':
                sortkey = 'category__name'
            if sortkey == 'price':
                sortkey = 'base_price'

            # Direction (ascending or descending)
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)

        # Filtering by category
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        # Filtering by subcategory
        if 'subcategory' in request.GET:
            subcategories = request.GET['subcategory'].split(',')
            products = products.filter(subcategory__name__in=subcategories)
            subcategories = SubCategory.objects.filter(name__in=subcategories)

        # Search query
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
    """ View to display products filtered by category """
    category = get_object_or_404(Category, name=category_name)
    products = Product.objects.filter(category=category)
    
    sort = None
    direction = None

    if request.GET:
        # Sorting
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            if sortkey == 'category':
                sortkey = 'category__name'
            if sortkey == 'price':
                sortkey = 'base_price'

            # Direction (ascending or descending)
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)

    current_sorting = f'{sort}_{direction}'
    
    context = {
        'category': category,
        'products': products,
        'current_sorting': current_sorting,
    }
    return render(request, 'products/products.html', context)

def subcategory_products(request, category_name, subcategory_name):
    """ View to display products filtered by subcategory """
    category = get_object_or_404(Category, name=category_name)
    subcategory = get_object_or_404(SubCategory, name=subcategory_name, category=category)
    products = Product.objects.filter(subcategory=subcategory)

    sort = None
    direction = None

    if request.GET:
        # Sorting
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            if sortkey == 'category':
                sortkey = 'category__name'
            if sortkey == 'price':
                sortkey = 'base_price'

            # Direction (ascending or descending)
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)

    current_sorting = f'{sort}_{direction}'

    context = {
        'category': category,
        'subcategory': subcategory,
        'products': products,
    }
    return render(request, 'products/products.html', context)

def product_detail(request, category_name, product_slug, subcategory_name=None):
    """ View to display detailed product information, including reviews """
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
    
    reviews = product.reviews.all()
    paginator = Paginator(reviews, 3)  # Paginate reviews (3 per page)
    page = request.GET.get('page', 1)
    try:
        reviews_page = paginator.get_page(page)
    except:
        reviews_page = paginator.get_page(1)

    # Get random products from the same category (excluding the current product)
    category_products = Product.objects.filter(
        category__name=category_name
    ).exclude(id=product.id)
    
    if category_products.count() < 3:
        other_products = Product.objects.exclude(
            Q(id=product.id) | Q(category__name=category_name)
        )
        all_products = list(category_products) + list(other_products)
        random_products = random.sample(all_products, min(4, len(all_products)))
    else:
        random_products = random.sample(list(category_products), min(4, category_products.count()))

    context = {
        'product': product,
        'random_products': random_products,
        'reviews': reviews_page,
        'user_has_reviewed': product.reviews.filter(user=request.user).exists() if request.user.is_authenticated else False
    }
    return render(request, 'products/product_detail.html', context)
