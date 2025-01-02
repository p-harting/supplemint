from django.urls import path
from . import views
from django.conf.urls import handler404


urlpatterns = [
    path('', views.index, name='home'),
    path('newsletter/subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),
]

handler404 = 'home.views.custom_404'
