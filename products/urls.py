from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_products, name='products'),
    path('<str:category_name>/', views.category_products, name='category_products'),
    path('<str:category_name>/<str:subcategory_name>/', views.subcategory_products, name='subcategory_products'),
    path('<str:category_name>/product/<slug:product_slug>/', views.product_detail, name='product_detail_no_subcategory'),
    path('<str:category_name>/<str:subcategory_name>/<slug:product_slug>/', views.product_detail, name='product_detail'),
]