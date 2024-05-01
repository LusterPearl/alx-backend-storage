#!/usr/bin/env python3
"""
Module for implementing an expiring web cache and trackers
using Redis.
"""
import requests
import redis
from functools import wraps
from typing import Callable

cache = redis.Redis()


def counter(method: Callable) -> Callable:
    """
    Fetches the HTML content of a given URL and caches it with an
    expiration time of 10 seconds.
    Args:
        url (str): The URL to fetch the content from.
    Returns:
        str: The HTML content of the URL.
    """
    @wraps(method)
    def wrapper(url) -> str:
        """ function wrapper """
        count_key = f"count:{url}"
        print(count_key)
        result_key = f"result:{url}"
        cache.incr(count_key)
        result = cache.get(result_key)
        if result:
            return result.decode('utf8')
        result = method(url)
        cache.set(count_key, 0)
        cache.setex(result_key, 10, result)
        return result
    return wrapper

@counter
def get_page(url: str) -> str:
    """ get a url response """
    return requests.get(url)