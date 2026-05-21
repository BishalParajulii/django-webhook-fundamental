from django.urls import path
from .webhook_views import receive_webhook
from .views import list_event

urlpatterns = [
    path('webhooks/receive/', receive_webhook),
    path('events/' , list_event)
]