#!/usr/bin/env python3
"""Module implementing a basic caching system
"""
from collections import OrderedDict
BaseCaching = __import__('base_caching').BaseCaching


class MRUCache(BaseCaching):
    """Class inheriting from BaseCaching class and implements a caching
    system that uses a Most Recently Used caching strategy to manage the
    items in the cache
    """
    def __init__(self):
        """Initializing the LRU cache"""
        super().__init__()
        self.order = []

    def put(self, key, item):
        """Stores key-value pair in the cache and discards most recently used
        item in cache if number of items is greater that BaseCaching.MAX_ITEMS
        """
        if key is not None and item is not None:
            if key in self.cache_data:
                self.order.remove(key)
            elif len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                most_recent_key = self.order.pop()
                del self.cache_data[most_recent_key]
                print(f"DISCARD: {most_recent_key}")

            self.cache_data[key] = item
            self.order.append(key)

    def get(self, key):
        """Gets the value associated with the key from cache"""
        if key is None or key not in self.cache_data:
            return None
        self.order.remove(key)
        self.order.append(key)
        return self.cache_data.get(key)
