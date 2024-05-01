#!/usr/bin/env python3
"""
Module for Cache class to interact with Redis
"""


import redis
import uuid
from typing import Callable, Union
from functools import wraps


class Cache:
    def __init__(self):
        """init self, count redis"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @staticmethod
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


    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Union string, int , float"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    @staticmethod
    def call_history(method: Callable) -> Callable:
        """Callable list"""
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            inputs_key = "{}:inputs".format(method.__qualname__)
            outputs_key = "{}:outputs".format(method.__qualname__)

            self._redis.rpush(inputs_key, str(args))
            output = method(self, *args, **kwargs)
            self._redis.rpush(outputs_key, output)

            return output
        return wrapper

    @classmethod
    def replay(cls, method: Callable) -> None:
        """Callable list"""
        inputs_key = "{}:inputs".format(method.__qualname__)
        outputs_key = "{}:outputs".format(method.__qualname__)

        inputs = cls._redis.lrange(inputs_key, 0, -1)
        outputs = cls._redis.lrange(outputs_key, 0, -1)

        print("{} was called {} times:".format(
            method.__qualname__, len(inputs)))

        for inp, out in zip(inputs, outputs):
            print("{}(*{}) -> {}".format(
                method.__qualname__, inp.decode(), out.decode()))

    def get(self, key: str, fn: Callable = None) -> Union[
            str, bytes, int, float]:
        """SELF, key, float, string"""
        data = self._redis.get(key)
        if data is None:
            return None
        if fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> str:
        """data (Union[str, bytes, int, float])"""
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> int:
        """data (Union[str, bytes, int, float])"""
        return self.get(key, fn=lambda d: int(d))