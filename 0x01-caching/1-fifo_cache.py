#!/usr/bin/env python3
"""Module implementing a basic caching system
"""
BaseCaching = __import__('base_caching').BaseCaching


class FIFOCache(BaseCaching):
    """Class inheriting from BaseCaching class and implements a caching
    system that uses a First in/First out caching strategy to manage the
    items in the cache
    """
    def __init__(self):
        """Initializing the cache"""
        super().__init__()

    def put(self, key, item):
        """Stores key-value pair in the cache and discards first item
        in cache if number of items is greater that BaseCaching.MAX_ITEMS
        """
        if key is not None and item is not None:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS \
                   and key not in self.cache_data.keys():
                first = next(iter(self.cache_data))
                del self.cache_data[first]
                print(f"DISCARD: {first}")
            self.cache_data[key] = item

    def get(self, key):
        """Gets the value associated with the key from cache"""
        if key is None or key not in self.cache_data.keys():
            return None
        return self.cache_data.get(key)
