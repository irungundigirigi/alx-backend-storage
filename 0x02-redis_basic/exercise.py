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

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        '''get and apply transformation fn on data if provided'''
        value = self._redis.get(key)
        if fn:
            value = fn(value)
        return value

    def get_str(self, key: str) -> str:
        ''' retrieve string value from cache '''
        value = self._redis.get(key)
        '''  decode byte string to string using utf-8 encoding '''
        return value.decode("utf-8")

    def get_int(self, key: str) -> int:
        ''' retrieve int value from cache '''
        value = self._redis.get(key)
        try:
            value = int(value.decode("utf-8"))
        except Exception:
            value = 0
        return value