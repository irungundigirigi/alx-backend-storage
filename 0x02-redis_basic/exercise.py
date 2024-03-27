#!/usr/bin/env python3
"""
Create Cache class and methods
"""
import redis
from typing import Callable, Union, Optional
from uuid import uuid4

class Cache:
    ''' Declares a Cache redis class '''
    def __init__(self):
        ''' Store an instance on initialization '''
        self._redis = redis.Redis(host='localhost', port=6379, db=0)
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        ''' takes a data argument and returns a string '''
        rkey = str(uuid4())
        self._redis.set(rkey, data)
        return rkey
