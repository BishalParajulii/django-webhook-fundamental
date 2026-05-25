import redis
import json
import uuid

redis_client = redis.Redis(host='localhost', port=6379, db=0)

QUEUE_NAME = 'my_queue'

def queue_webhook(event_type , data):
    
    payload = {
        "event_id" : str(uuid.uuid4()),
        "event_type" : event_type,
        "data" : data,
    }
    
    redis_client.lpush(QUEUE_NAME , json.dumps(payload))
    
#lpush adds to the left of the list