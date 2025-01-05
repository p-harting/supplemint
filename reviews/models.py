from django.db import models
from django.db.models import Avg
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from products.models import Product

class Review(models.Model):
    # Foreign key to Product, allowing multiple reviews per product
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    
    # Foreign key to User, allowing multiple reviews per user
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    
    # Rating field with validation for values between 1 and 5
    rating = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )
    
    # Review text with a maximum length of 300 characters
    text = models.TextField(max_length=300)
    
    # Boolean field to track if the review is approved
    approved = models.BooleanField(default=False)
    
    # Timestamps for creation and last update
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Ensures a user can only leave one review per product
        unique_together = ('product', 'user')
        
        # Orders reviews by creation date, newest first
        ordering = ['-created_at']

    def __str__(self):
        """
        Returns a string representation of the review.
        Includes the username, product name, and rating.
        """
        return f'{self.user.username} - {self.product.name} - {self.rating}★'

    def save(self, *args, **kwargs):
        """
        Saves the review and updates the product rating if the review is approved.
        If the approval status changes, the product rating is recalculated.
        """
        if self.pk:
            old_review = Review.objects.get(pk=self.pk)
            if old_review.approved != self.approved:
                super().save(*args, **kwargs)
                self.update_product_rating()
                return
        
        super().save(*args, **kwargs)
        if self.approved:
            self.update_product_rating()

    def update_product_rating(self):
        """
        Updates the product's average rating based on approved reviews.
        If no approved reviews exist, the rating is set to 0.
        """
        approved_reviews = Review.objects.filter(product=self.product, approved=True)
        if approved_reviews.exists():
            avg_rating = approved_reviews.aggregate(Avg('rating'))['rating__avg']
            self.product.rating = round(avg_rating, 1)
        else:
            self.product.rating = 0
        self.product.save()
