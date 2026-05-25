"""

Currently Not Used


import json
import hmac
import hashlib
import uuid
import requests
from django.conf import settings



def send_webhook(event_type, data):
    payload = {
        'event_id': str(uuid.uuid4()),
        'event_type': event_type,
        'data': data,
    }

    body = json.dumps(payload)

    hash_code = hmac.new(settings.WEBHOOK_SECRET.encode(), body.encode(), hashlib.sha256)
    signature = hash_code.hexdigest()

    try:
        requests.post(
            settings.WEBHOOK_TARGET_URL,
            data=body,
            headers={
                'Content-Type': 'application/json',
                'X-Webhook-Signature': signature,
            },
            timeout=5,
        )
        print(f"[Webhook] '{event_type}' sent")
    except Exception as e:
        print(f"[Webhook] Failed: {e}")
        
        
        
"""