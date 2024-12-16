from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse
from django.core.exceptions import ValidationError
from ckeditor_uploader.fields import RichTextUploadingField


class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = RichTextUploadingField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    meta_description = models.CharField(max_length=160, blank=True, help_text="Meta description for SEO (max 160 characters)")
    meta_keywords = models.CharField(max_length=200, blank=True, help_text="Comma-separated keywords for SEO")
    featured_image = models.ImageField(upload_to='blog_images/', blank=True, null=True, help_text="Featured image for the blog post")
    is_published = models.BooleanField(default=False, help_text="Check to publish the post")

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})
    
    def clean(self):
        if Post.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
            raise ValidationError({'slug': 'This slug is already in use.'})
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        self.clean()
        super().save(*args, **kwargs)