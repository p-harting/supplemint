from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg
from products.models import Product
from .models import Review
from .forms import ReviewForm
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.core.paginator import Paginator


@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    
    existing_review = Review.objects.filter(user=request.user, product=product).first()
    if existing_review:
        form = ReviewForm(instance=existing_review)
        context = {'form': form, 'review': existing_review, 'is_edit': True}
        form_html = render_to_string('reviews/review_form.html', context, request=request)
        return JsonResponse({'form_html': form_html, 'is_edit': True, 'review_id': existing_review.id})

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product
            review.save()

            avg_rating = Review.objects.filter(product=product, approved=True).aggregate(Avg('rating'))['rating__avg']
            product.rating = round(avg_rating, 1)
            product.save()
            
            messages.success(request, 'Thank you for your review!')
            return JsonResponse({'success': True})
    else:
        form = ReviewForm()

    context = {'form': form, 'product': product}
    form_html = render_to_string('reviews/review_form.html', context, request=request)
    return JsonResponse({'form_html': form_html})

@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()

            avg_rating = Review.objects.filter(product=product, approved=True).aggregate(Avg('rating'))['rating__avg']
            review.product.rating = round(avg_rating, 1)
            review.product.save()
            
            messages.success(request, 'Review updated successfully!')
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    else:
        form = ReviewForm(instance=review)
    
    context = {'form': form, 'review': review, 'is_edit': True}
    form_html = render_to_string('reviews/review_form.html', context, request=request)
    return JsonResponse({'form_html': form_html})

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    
    if request.method == 'POST':
        product = review.product
        review.delete()
        avg_rating = Review.objects.filter(product=product, approved=True).aggregate(Avg('rating'))['rating__avg']
        product.rating = round(avg_rating or 0, 1)
        product.save()
        
        messages.success(request, 'Review deleted successfully!')
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False}, status=400)

def sort_reviews(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    sort_option = request.GET.get('sort', 'newest')
    page = request.GET.get('page', 1)
    
    reviews = product.reviews.all()
    
    if sort_option == 'oldest':
        reviews = reviews.order_by('created_at')
    elif sort_option == 'rating_high':
        reviews = reviews.order_by('-rating')
    elif sort_option == 'rating_low':
        reviews = reviews.order_by('rating')
    else:
        reviews = reviews.order_by('-created_at')
    
    paginator = Paginator(reviews, 3)
    try:
        reviews_page = paginator.get_page(page)
    except:
        reviews_page = paginator.get_page(1)
    
    context = {
        'product': product,
        'reviews': reviews_page,
        'user': request.user,
        'user_has_reviewed': product.reviews.filter(user=request.user).exists() if request.user.is_authenticated else False
    }
    
    html = render_to_string('reviews/partials/review_list.html', context, request=request)
    return JsonResponse({
        'html': html,
        'has_next': reviews_page.has_next(),
        'has_previous': reviews_page.has_previous(),
        'current_page': reviews_page.number,
        'total_pages': paginator.num_pages
    })