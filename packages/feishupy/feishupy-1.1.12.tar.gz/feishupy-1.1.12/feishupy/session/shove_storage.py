# -*- coding: utf-8 -*-
from . import SessionStorage


class ShoveStorage(SessionStorage):
    def __init__(self, shove):
        self.shove = shove

    def get(self, key, default=None):
        try:
            return self.shove[key]
        except KeyError:
            return default

    def set(self, key, value, ttl=None):
        if value is None:
            return
        self.shove[key] = value

    def delete(self, key):
        try:
            del self.shove[key]
        except KeyError:
            pass
