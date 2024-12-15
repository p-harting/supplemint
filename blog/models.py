from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})
    
    def clean(self):
        if Post.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
            raise ValidationError({'slug': 'This slug is already in use.'})
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)