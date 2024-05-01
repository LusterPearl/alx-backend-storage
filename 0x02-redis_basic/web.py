#!/usr/bin/env python3
"""
Module for implementing an expiring web cache and trackers
using Redis.
"""

import requests
import redis
import time
from functools import wraps


"""Connect to Redis"""
redis_client = redis.Redis()


def get_page(url: str) -> str:
    """
    Fetches the HTML content of a given URL and caches it with an
    expiration time of 10 seconds.
    Args:
        url (str): The URL to fetch the content from.
    Returns:
        str: The HTML content of the URL.
    """
    url_count_key = f"count:{url}"
    redis_client.incr(url_count_key)

    """Cache the result with an expiration time of 10 seconds"""
    cache_key = f"cache:{url}"
    cached_content = redis_client.get(cache_key)
    if cached_content:
        return cached_content.decode()

    response = requests.get(url)
    if response.status_code == 200:
        content = response.text
        redis_client.setex(cache_key, 10, content)
        return content
    else:
        return f"Failed to fetch URL: {url}"
