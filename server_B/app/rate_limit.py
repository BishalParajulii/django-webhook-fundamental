import time

request_times = []

# 5 requests per 10 seconds
RATE_LIMIT = 5
WINDOW = 10


# Simple in-memory rate limiter
def is_rate_limited(request):

    global request_times
    now = time.time()
    
    request_times[:] = [t for t in request_times if now - t < WINDOW]
    if len(request_times) >= RATE_LIMIT:
        print("[Rate Limit] Too many requests! Returning 429.")
        return True
    request_times.append(now)
    print(f"[Rate Limit] Request allowed. {len(request_times)}/{RATE_LIMIT} in window.")
    return False