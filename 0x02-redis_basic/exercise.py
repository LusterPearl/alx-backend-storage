#!/usr/bin/env python3
"""
Module for Cache class to interact with Redis
"""

import redis
import uuid
from typing import Union, Callable
from functools import wraps


class Cache:
    def __init__(self):
        """Initialize the Cache class."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @staticmethod
    def count_calls(method: Callable) -> Callable:
        """Decorator to count how many times a method is called."""
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            key = method.__qualname__
            self._redis.incr(key)
            return method(self, *args, **kwargs)
        return wrapper

    @staticmethod
    def call_history(method: Callable) -> Callable:
        """Decorator to store the history of inputs"""
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            inputs_key = "{}:inputs".format(method.__qualname__)
            outputs_key = "{}:outputs".format(method.__qualname__)

            self._redis.rpush(inputs_key, str(args))
            output = method(self, *args, **kwargs)
            self._redis.rpush(outputs_key, output)

            return output
        return wrapper

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store data in Redis using a randomly generated key."""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) -> Union[str, bytes, int, float]:
        """Retrieve data from Redis and optionally"""
        data = self._redis.get(key)
        if data is None:
            return None
        if fn is not None:
            return fn(data)
        return data

    @classmethod
    def replay(cls, method: Callable) -> None:
        """Display the history of calls of a particular function."""
        inputs_key = "{}:inputs".format(method.__qualname__)
        outputs_key = "{}:outputs".format(method.__qualname__)

        inputs = cls._redis.lrange(inputs_key, 0, -1)
        outputs = cls._redis.lrange(outputs_key, 0, -1)

        print("{} was called {} times:".format(
            method.__qualname__, len(inputs)))

        for inp, out in zip(inputs, outputs):
            print("{}(*{}) -> {}".format(
                method.__qualname__, inp.decode(), out.decode()))