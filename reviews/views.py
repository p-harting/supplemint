from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg
from products.models import Product
from .models import Review
from .forms import ReviewForm

@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    
    if Review.objects.filter(user=request.user, product=product).exists():
        messages.error(request, 'You have already reviewed this product.')
        if product.subcategory:
            return redirect('product_detail', 
                          category_name=product.category.name,
                          subcategory_name=product.subcategory.name,
                          product_slug=product.slug)
        else:
            return redirect('product_detail_no_subcategory',
                          category_name=product.category.name,
                          product_slug=product.slug)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product
            review.save()
            
            avg_rating = Review.objects.filter(product=product).aggregate(
                Avg('rating'))['rating__avg']
            product.rating = round(avg_rating, 1)
            product.save()
            
            messages.success(request, 'Thank you for your review!')
            if product.subcategory:
                return redirect('product_detail', 
                              category_name=product.category.name,
                              subcategory_name=product.subcategory.name,
                              product_slug=product.slug)
            else:
                return redirect('product_detail_no_subcategory',
                              category_name=product.category.name,
                              product_slug=product.slug)
    else:
        form = ReviewForm()

    return render(request, 'reviews/add_review.html', {
        'form': form,
        'product': product
    })