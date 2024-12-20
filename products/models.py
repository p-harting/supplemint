from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField

class Category(models.Model):
    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)
    description = RichTextField(null=True, blank=True)
    seo_title = models.CharField(max_length=60, null=True, blank=True)
    seo_meta_description = models.CharField(max_length=160, null=True, blank=True)
    seo_keywords = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name

class SubCategory(models.Model):
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)
    description = RichTextField(null=True, blank=True)
    seo_title = models.CharField(max_length=60, null=True, blank=True)
    seo_meta_description = models.CharField(max_length=160, null=True, blank=True)
    seo_keywords = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name

class Product(models.Model):
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
    subcategory = models.ForeignKey('SubCategory', null=True, blank=True, on_delete=models.SET_NULL)
    sku = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    description = models.TextField()
    detailed_description = RichTextField(null=True, blank=True)
    has_sizes = models.BooleanField(default=False, null=True, blank=True)
    base_price = models.DecimalField(max_digits=6, decimal_places=2)
    stock = models.IntegerField(default=0)
    rating = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    nutritional_info = RichTextField(null=True, blank=True)
    how_to_use = models.TextField(null=True, blank=True)
    key_facts = models.JSONField(null=True, blank=True) 
    slug = models.SlugField(max_length=254, unique=True, null=True, blank=True)

    @property
    def price(self):
        if not self.has_sizes:
            return self.base_price
        size_prices = self.sizes.all()
        return min([size.price for size in size_prices]) if size_prices else self.base_price
    
    def get_stock_display(self):
        if self.has_sizes:
            return sum(size.stock for size in self.sizes.all())
        return self.stock

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class ProductSize(models.Model):
    product = models.ForeignKey('Product', related_name='sizes', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    stock = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.product.name} - {self.name}"

    class Meta:
        unique_together = ('product', 'name')