import os
import time

from cache_gs.cache_classes.file_cache import FileCache
from cache_gs.cache_classes.redis_cache import RedisCache
from cache_gs.cache_classes.sqlite_cache import SQLiteCache
from cache_gs.interfaces.super_cache import CacheException, SuperCache


class CacheGS(SuperCache):
    """
    Create your cache of section, key, values

    Using filesystem:

    cache = CacheGS('path://directory_for_cache_storage')

    Using sqlite

    cache = CacheGS('sqlite://directory_or_file_for_storage')

    Using redis:

    cache = CacheGS('redis://host:6379?arg=value&arg2=value2')

    args: 
        username
        password
        client_name
        encoding
        encoding_errors
        charset
        db
        health_check_interval

        More informations on args for redis: https://github.com/andymccurdy/redis-py
    """

    CACHE_CLASSES = {
        'path': FileCache,
        'redis': RedisCache,
        'sqlite': SQLiteCache
    }

    def __init__(self, string_connection: str):        
        string_connection = str(string_connection)
        self._cache: SuperCache = None

        schema = (string_connection+':').split(':')[0]

        if schema not in self.CACHE_CLASSES:
            raise CacheException(
                'unexpected cache schema "{0}"'.format(schema))

        self._cache = self.CACHE_CLASSES[schema](string_connection)

    def get_value(self, section: str, key: str, default=None) -> str:
        return self._cache.get_value(section, key, default)

    def set_value(self, section: str, key: str, value: str, valid_until: int = 0, expires_in: int = 0) -> bool:
        if expires_in > 0:
            valid_until = int(time.time())+expires_in

        return self._cache.set_value(section, key, value, valid_until)

    def delete_value(self, section: str, key: str) -> bool:
        """"Delete data from cache"""
        return self._cache.delete_value(section, key)

    def purge_expired(self):
        """Forces removing expired data"""
        return self._cache.purge_expired()
