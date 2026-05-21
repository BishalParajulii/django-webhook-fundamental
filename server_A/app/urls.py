

from django.urls import path
from .views import create_product , create_order
urlpatterns = [
    path('products/' , create_product , name='create'),
    path('orders/' , create_order , name='create_order'),
]
