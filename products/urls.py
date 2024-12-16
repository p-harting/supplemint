from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_products, name='products'),
    path('<str:category_name>/', views.category_products, name='category_products'),
    path('<str:category_name>/<slug:product_slug>/', views.product_detail, name='product_detail'),
]