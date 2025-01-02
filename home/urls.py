from django.urls import path
from . import views
from django.conf.urls import handler404


urlpatterns = [
    path('', views.index, name='home'),
    path('newsletter/subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),
    path('shipping/', views.shipping, name='shipping'),
    path('returns/', views.returns, name='returns'),
    path('privacy/', views.privacy, name='privacy'),
    path('terms/', views.terms, name='terms'),
]

handler404 = 'home.views.custom_404'
