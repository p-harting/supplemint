from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse
from django.core.exceptions import ValidationError
from ckeditor_uploader.fields import RichTextUploadingField


class Post(models.Model):
    # Title of the blog post
    title = models.CharField(max_length=200)

    # Slug for URL, unique for each post
    slug = models.SlugField(unique=True)

    # Author of the post, linked to the User model
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # Content of the post using a rich text field
    content = RichTextUploadingField()

    # Timestamps for when the post is created and updated
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # SEO-related fields
    meta_description = models.CharField(
        max_length=160, blank=True,
        help_text="Meta description for SEO (max 160 characters)")
    meta_keywords = models.CharField(
        max_length=200, blank=True,
        help_text="Comma-separated keywords for SEO")

    # Featured image for the post
    featured_image = models.ImageField(
        upload_to='blog_images/', blank=True, null=True,
        help_text="Featured image for the blog post")

    # Flag to determine if the post is published or not
    is_published = models.BooleanField(
        default=False, help_text="Check to publish the post")

    def __str__(self):
        # String representation of the post
        return self.title

    def get_absolute_url(self):
        # Returns the absolute URL of the post
        return reverse('post_detail', kwargs={'slug': self.slug})

    def clean(self):
        # Custom validation to ensure the slug is unique
        if Post.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
            raise ValidationError({'slug': 'This slug is already in use.'})

    def save(self, *args, **kwargs):
        # Automatically generate slug from title if not provided
        if not self.slug:
            self.slug = slugify(self.title)
        # Run custom validation
        self.clean()

        # Save the post to the database
        super().save(*args, **kwargs)
