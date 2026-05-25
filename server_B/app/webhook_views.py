from django.shortcuts import render
import hmac
import hashlib
from .models import WebhookEvent
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import JsonResponse , HttpResponseBadRequest
import json
from .rate_limit import is_rate_limited


@csrf_exempt
def receive_webhook(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Invalid request method")
    
    if is_rate_limited(request):
        print("Rate limit exceeded")
        return JsonResponse({'error' : 'Too many requests'} , status=429)
    
    incomming_signature = request.headers.get('X-Webhook-Signature', '')
    body = request.body 
    
    expected_signature = hmac.new(
        settings.WEBHOOK_SECRET.encode(),
        body,
        hashlib.sha256
    ).hexdigest()
    
    if not hmac.compare_digest(incomming_signature , expected_signature):
        print("Invalid Signature")
        return JsonResponse({'error' : 'Invalid Signature'})
    
    payload = json.loads(body)
    event_id = payload.get('event_id')
    event_type = payload.get('event_type')
    
    if WebhookEvent.objects.filter(event_id=event_id).exists():
        print("Duplicate value")
        return JsonResponse({'status' : 'duplicate value'})
    
    WebhookEvent.objects.create(
        event_id=event_id,
        event_type=event_type,
        payload=payload
    )
    
    if event_type == 'product.created':
        print(f"[Webhook]  New product: {payload['data']['name']}")
        
    return JsonResponse({'status' : "received"})