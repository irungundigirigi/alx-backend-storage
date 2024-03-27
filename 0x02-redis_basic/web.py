#!/usr/bin/env python3
"""
A web cache and tracker
"""
import requests
import redis
from functools import wraps

# Redis connection
redis_store = redis.Redis()


def count_url_access(method):
    """Decorator counting how many times
    a URL is accessed"""
    @wraps(method)
    def wrapper(url):
        cached_key = "cached:" + url
        cached_data = redis_store.get(cached_key)
        if cached_data:
            return cached_data.decode("utf-8")

        count_key = "count:" + url
        html_content = method(url)

        redis_store.incr(count_key)
        redis_store.set(cached_key, html_content)
        redis_store.expire(cached_key, 10)
        return html_content
    return wrapper


@count_url_access
def get_page(url: str) -> str:
    """Returns HTML content of a URL"""
    response = requests.get(url)
    return response.text

