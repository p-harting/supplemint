from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from products.models import Product
from .models import Review
from .forms import ReviewForm

@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    
    # Check if user already reviewed this product
    if Review.objects.filter(user=request.user, product=product).exists():
        messages.error(request, 'You have already reviewed this product.')
        return redirect('product_detail', product.id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product
            review.save()
            
            # Update product's average rating
            avg_rating = Review.objects.filter(product=product).aggregate(
                Avg('rating'))['rating__avg']
            product.rating = round(avg_rating, 1)
            product.save()
            
            messages.success(request, 'Thank you for your review!')
            return redirect('product_detail', product.id)
    else:
        form = ReviewForm()

    return render(request, 'reviews/add_review.html', {
        'form': form,
        'product': product
    })