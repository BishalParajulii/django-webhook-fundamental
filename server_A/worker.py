import redis
import json
import time
import requests
import hmac
import hashlib
import uuid


import os
import django

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "server_A.settings"
)

django.setup()

from django.conf import settings



r = redis.Redis(host='localhost', port=6379, db=0)

QUEUE_NAME = "my_queue"


RATE_LIMIT = 5     
WINDOW = 10      

request_times = [] 




def allowed():
    global request_times

    now = time.time()

    
    request_times = [
        t for t in request_times
        if now - t < WINDOW
    ]

    if len(request_times) < RATE_LIMIT:
        request_times.append(now)
        return True

    return False



def send_request(task):
    url = "http://localhost:8001/webhooks/receive/"
    payload = {
        "event_id": task["event_id"],
        "event_type": task["event_type"],
        "data": task["data"],
    }
    body = json.dumps(payload , separators=(',', ':'))
    
    signature  = hmac.new(settings.WEBHOOK_SECRET.encode() , body.encode(), hashlib.sha256).hexdigest()

    try:
        res = requests.post(url, data=body,  headers={
            "Content-Type": "application/json",
            "X-Webhook-Signature": signature,
        }, timeout=5)


        if res.status_code == 200:
            print("[SUCCESS] Sent request")
        elif res.status_code == 429:
            retry_after = int(res.headers.get("Retry-After", 5))
            print(f"[RATE LIMITED] Sleeping {retry_after}s and pausing worker")
            task["retry_count"] = task.get("retry_count", 0) + 1
            r.lpush(QUEUE_NAME, json.dumps(task))
            time.sleep(retry_after)
        elif res.status_code >= 500:
            print("[SERVER ERROR] Retrying later")
            time.sleep(5)
            task["retry_count"] = task.get("retry_count", 0) + 1
            r.lpush(QUEUE_NAME, json.dumps(task))
        else:
            print(f"[FAILED] Status: {res.status_code}")

    except Exception as e:
        print(f"[ERROR] {e}")
        time.sleep(5)
        task["retry_count"] = task.get("retry_count", 0) + 1
        r.lpush(QUEUE_NAME, json.dumps(task))


def worker():
    print("Worker started...")

    while True:

        _, raw = r.brpop(QUEUE_NAME)
        task = json.loads(raw)

        # wait if rate limit exceeded
        while not allowed():
            print("[RATE LIMIT] Waiting...")
            time.sleep(1)

        send_request(task)



if __name__ == "__main__":
    worker()