from django.urls import path
from . import views

urlpatterns = [
    path('manage/', views.product_management, name='product_management'),
    path('add/', views.add_product, name='add_product'),
    path('edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete/<int:product_id>/', views.delete_product,
         name='delete_product'),
    path('', views.all_products, name='products'),
    path(
        '<str:category_name>/', views.category_products,
        name='category_products'),
    path(
        '<str:category_name>/<str:subcategory_name>/',
        views.subcategory_products, name='subcategory_products'),
    path(
        '<str:category_name>/product/<slug:product_slug>/',
        views.product_detail, name='product_detail_no_subcategory'),
    path(
        '<str:category_name>/<str:subcategory_name>/<slug:product_slug>/',
        views.product_detail, name='product_detail'),
]
