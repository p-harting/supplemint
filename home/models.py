from django.db import models
from ckeditor.fields import RichTextField

class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

class NewsletterEmail(models.Model):
    subject = models.CharField(max_length=255)
    content = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject

class PageContent(models.Model):
    PAGE_CHOICES = [
        ('shipping', 'Shipping Information'),
        ('returns', 'Returns Policy'),
        ('privacy', 'Privacy Policy'),
        ('terms', 'Terms & Conditions'),
    ]
    
    page = models.CharField(max_length=50, choices=PAGE_CHOICES, unique=True)
    content = RichTextField()
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.get_page_display()
