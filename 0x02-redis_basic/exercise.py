#!/usr/bin/env python3
"""
Main file
"""

import redis
import uuid
from functools import wraps
from typing import Callable


def count_calls(fn: Callable) -> Callable:
    """
    Decorator to count how many times a method is called
    """
    @wraps(fn)
    def wrapped(self, *args, **kwargs):
        key = fn.__qualname__
        self._redis.incr(key)
        return fn(self, *args, **kwargs)
    return wrapped

class Cache:
    """
    Cache class to store and retrieve data from Redis
    """

    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data):
        """
        Store data in Redis and return the generated key
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key, fn=None):
        """
        Retrieve data from Redis and optionally apply a conversion function
        """
        data = self._redis.get(key)
        if data is None:
            return None
        if fn:
            return fn(data)
        return data


if __name__ == '__main__':
    cache = Cache()

    cache.store(b"first")
    print(cache.get(cache.store.__qualname__))

    cache.store(b"second")
    cache.store(b"third")
    print(cache.get(cache.store.__qualname__))
