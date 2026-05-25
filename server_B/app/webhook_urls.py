from django.urls import path
from .webhook_views import receive_webhook

urlpatterns = [
    path('webhooks/receive/', receive_webhook),
    
]