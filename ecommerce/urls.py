from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.views.generic.base import TemplateView, RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage
from django.contrib.sitemaps.views import sitemap
from .sitemaps import (
    StaticViewSitemap,
    BlogSitemap,
    ProductSitemap,
    CategorySitemap,
    SubCategorySitemap
)

sitemaps = {
    'static': StaticViewSitemap,
    'blog': BlogSitemap,
    'products': ProductSitemap,
    'categories': CategorySitemap,
    'subcategories': SubCategorySitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('home.urls')),
    path('products/', include('products.urls')),
    path('bag/', include('bag.urls')),
    path('checkout/', include('checkout.urls')),
    path('profile/', include('profiles.urls')),
    path('contact/', include('contact.urls')),
    path('blog/', include('blog.urls')),
    path('referrals/', include('referrals.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('reviews/', include('reviews.urls')),
    path('robots.txt', RedirectView.as_view(url=staticfiles_storage.url('robots.txt'))),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
