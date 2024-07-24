#!/usr/bin/env python3
"""Module implementing a basic caching system
"""
from collections import OrderedDict
BaseCaching = __import__('base_caching').BaseCaching


class LRUCache(BaseCaching):
    """Class inheriting from BaseCaching class and implements a caching
    system that uses a Last Recently Used caching strategy to manage the
    items in the cache
    """
    def __init__(self):
        """Initializing the LRU cache"""
        super().__init__()
        self.cache_data = OrderedDict()

    def put(self, key, item):
        """Stores key-value pair in the cache and discards least recently used
        item in cache if number of items is greater that BaseCaching.MAX_ITEMS
        """
        if key is not None and item is not None:
            if key in self.cache_data:
                self.cache_data.move_to_end(key)
            self.cache_data[key] = item
            if len(self.cache_data) > BaseCaching.MAX_ITEMS:
                discarded_key, _ = self.cache_data.popitem(last=False)
                print(f"DISCARD: {discarded_key}")

    def get(self, key):
        """Gets the value associated with the key from cache"""
        if key is None or key not in self.cache_data.keys():
            return None
        value = self.cache_data[key]
        self.cache_data.move_to_end(key)
        return value
