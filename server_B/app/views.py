from django.http import JsonResponse
from .models import WebhookEvent



def list_event(request):
    event = WebhookEvent.objects.all().values(
        'event_id' , 'event_type' , 'received_at' )
    
    return JsonResponse({'events' : list(event)})

