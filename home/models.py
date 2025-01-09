from django.db import models
from ckeditor.fields import RichTextField


class NewsletterSubscriber(models.Model):
    """Model representing a subscriber to the newsletter."""
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return the email of the subscriber as the string representation."""
        return self.email


class NewsletterEmail(models.Model):
    """Model representing an email sent to newsletter subscribers."""
    subject = models.CharField(max_length=255)
    content = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return the subject of the email as the string representation."""
        return self.subject


class PageContent(models.Model):
    """Model representing content for different pages like
    Terms, Privacy, etc."""
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
        """Return the display name of the page as the string representation."""
        return self.get_page_display()
