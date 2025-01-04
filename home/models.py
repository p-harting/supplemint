from django.db import models
from ckeditor.fields import RichTextField

class NewsletterSubscriber(models.Model):
    """Model representing a subscriber to the newsletter."""
    
    email = models.EmailField(unique=True)  # Email field, unique to avoid duplicates
    subscribed_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the subscriber joined

    def __str__(self):
        """Return the email of the subscriber as the string representation."""
        return self.email

class NewsletterEmail(models.Model):
    """Model representing an email sent to newsletter subscribers."""
    
    subject = models.CharField(max_length=255)  # Subject of the newsletter email
    content = RichTextField()  # Rich text content of the email
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the email was created

    def __str__(self):
        """Return the subject of the email as the string representation."""
        return self.subject

class PageContent(models.Model):
    """Model representing content for different pages like Terms, Privacy, etc."""
    
    PAGE_CHOICES = [
        ('shipping', 'Shipping Information'),
        ('returns', 'Returns Policy'),
        ('privacy', 'Privacy Policy'),
        ('terms', 'Terms & Conditions'),
    ]
    
    page = models.CharField(max_length=50, choices=PAGE_CHOICES, unique=True)  # Page type (e.g., 'shipping', 'returns')
    content = RichTextField()  # Rich text content for the page
    last_updated = models.DateTimeField(auto_now=True)  # Timestamp when the content was last updated

    def __str__(self):
        """Return the display name of the page as the string representation."""
        return self.get_page_display()  # Get the human-readable name of the page from choices
