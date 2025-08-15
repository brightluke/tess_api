import redis
import os
import json
from typing import Optional

redis_client = redis.Redis(
    host=os.getenv('REDIS_HOST', 'localhost'),
    port=6379,
    db=0,
    decode_responses=True
)

def get_cached_quote(personality: str, filters: dict) -> Optional[dict]:
    cache_key = f"quote:{personality}:{hash(frozenset(filters.items()))}"
    return redis_client.get(cache_key)

def cache_quote(cache_key: str, quote: dict, ttl=300):
    redis_client.setex(cache_key, ttl, json.dumps(quote))