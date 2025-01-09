from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from blog.models import Post
from products.models import Product, Category, SubCategory


class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'weekly'

    def items(self):
        return ['home', 'shipping', 'returns', 'privacy', 'terms']

    def location(self, item):
        return reverse(item)


class BlogSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return Post.objects.all()

    def location(self, obj):
        return reverse('post_detail', args=[obj.slug])


class ProductSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Product.objects.all()

    def location(self, obj):
        if obj.subcategory:
            return reverse(
                'product_detail',
                args=[obj.category.name, obj.subcategory.name, obj.slug])
        return reverse(
            'product_detail_no_subcategory',
            args=[obj.category.name, obj.slug])


class CategorySitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return Category.objects.all()

    def location(self, obj):
        return reverse('category_products', args=[obj.name])


class SubCategorySitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return SubCategory.objects.all()

    def location(self, obj):
        return reverse(
            'subcategory_products',
            args=[obj.category.name, obj.name])
