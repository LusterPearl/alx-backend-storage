#!/usr/bin/env python3
"""
Module for implementing an expiring web cache and trackers
using Redis.
"""

import requests
import redis
import time
from functools import wraps


r = redis.Redis(host='localhost', port=6379, db=0)


def track_access(url):
    """Increment the access count for a given URL."""
    r.incr(f"count:{url}")


def get_page(url):
    """Retrieve the HTML content of a URL, track access count"""

    cached_content = r.get(url)
    if cached_content:
        return cached_content.decode('utf-8')

    response = requests.get(url)
    page_content = response.text

    track_access(url)
    r.setex(url, 10, page_content)
    return page_content
