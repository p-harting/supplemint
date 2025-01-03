from django.db import models
from django.db.models import Avg
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from products.models import Product

class Review(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    rating = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )
    text = models.TextField(max_length=300)
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('product', 'user')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} - {self.product.name} - {self.rating}★'

    def save(self, *args, **kwargs):
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
        approved_reviews = Review.objects.filter(product=self.product, approved=True)
        if approved_reviews.exists():
            avg_rating = approved_reviews.aggregate(Avg('rating'))['rating__avg']
            self.product.rating = round(avg_rating, 1)
        else:
            self.product.rating = 0
        self.product.save()
