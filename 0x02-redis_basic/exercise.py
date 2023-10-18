#!/usr/bin/env python3
"""
Main file
"""
import redis
import uuid
from typing import Union

class Cache:
    """
    Cache class to store data in Redis
    """

    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store data in Redis and return the generated key
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

if __name__ == '__main__':
    cache = Cache()

    data = b"hello"
    key = cache.store(data)
    print(key)

    local_redis = redis.Redis()
    print(local_redis.get(key))
