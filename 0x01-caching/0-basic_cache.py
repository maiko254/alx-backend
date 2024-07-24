#!/usr/bin/env python3
"""Module implementing a basic caching system """
BaseCaching = __import__('base_caching').BaseCaching


class BasicCache(BaseCaching):
    """Class inheriting from BaseCaching class and implements a caching
    system
    """
    def __init__(self):
        """Initializing the cache"""
        super().__init__()

    def put(self, key, item):
        """Stores key-value pair in the cache"""
        if key is not None and item is not None:
            self.cache_data[key] = item

    def get(self, key):
        """Gets the value associated with the key from cache"""
        if key is None or key not in self.cache_data.keys():
            return None
        return self.cache_data.get(key)
