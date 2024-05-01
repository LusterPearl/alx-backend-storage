#!/usr/bin/env python3
"""
Module for Cache class to interact with Redis
"""

from typing import Callable, Union
from functools import wraps
import redis
import uuid


class Cache:
    def __init__(self):
        """init self, count redis"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def count_calls(method: Callable) -> Callable:
        """
        Store data in Redis using a randomly generated key

        Args:
            data (Union[str, bytes, int, float]): The data to store

        Returns:
            str: The key under which the data is stored
        """
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            key = method.__qualname__
            self._redis.incr(key)
            return method(self, *args, **kwargs)
        return wrapper

    @call_history
    def store(self, data: str) -> str:
        """Store data in Redis using a randomly generated key"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get_inputs(self, method_name: str):
        """Retrieve the inputs for a method from Redis"""
        inputs_key = "{}:inputs".format(method_name)
        return self._redis.lrange(inputs_key, 0, -1)

    def get_outputs(self, method_name: str):
        """Retrieve the outputs for a method from Redis"""
        outputs_key = "{}:outputs".format(method_name)
        return self._redis.lrange(outputs_key, 0, -1)
    
    def replay(cache, method):
        """Display the history of calls of a particular function"""
    inputs = cache.get_inputs(method.__qualname__)
    outputs = cache.get_outputs(method.__qualname__)

    print("{} was called {} times:".format(method.__qualname__, len(inputs)))

    for inp, out in zip(inputs, outputs):
        print(
        "{}(*{}) -> {}".format(
            method.__qualname__,
            inp.decode(),
            out.decode()
        )
    )