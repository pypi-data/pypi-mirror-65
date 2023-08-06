# -*- coding: utf-8 -*-

from . import SessionStorage


class RedisStorage(SessionStorage):
    def __init__(self, redis):
        for method_name in ("get", "set", "delete"):
            assert hasattr(redis, method_name)
        self.redis = redis

    def get(self, key, default=None):
        value = self.redis.get(key)
        if value is None:
            return default
        return value

    def set(self, key, value, ttl=None):
        if value is None:
            return
        self.redis.set(key, value, ex=ttl)

    def delete(self, key):
        self.redis.delete(key)
