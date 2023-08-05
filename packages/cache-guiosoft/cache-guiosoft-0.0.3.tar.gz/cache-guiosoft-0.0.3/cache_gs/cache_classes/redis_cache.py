from time import time

from redis import Redis

from cache_gs.cache_classes.cache_data import CacheData
from cache_gs.cache_classes.redis_setup import RedisSetup
from cache_gs.interfaces.super_cache import SuperCache


class RedisCache(SuperCache):
    """
    Connection string
    redis://localhost:6379?ConnectTimeout=5000&IdleTimeOutSecs=180
    """

    def setup(self):
        self.redis_setup: RedisSetup = RedisSetup(self._string_connection)
        self.redis: Redis = Redis(**self.redis_setup.options)

    def _get_value(self, section: str, key: str, default=None) -> CacheData:
        value = self.redis.get(self.section_key(section, key))
        if value:
            return CacheData(section, key, value.decode(self.redis_setup.encoding), 0)
        return CacheData(section, key, default, 0)

    def _set_value(self, data: CacheData) -> bool:
        if data.expires_in > 0:
            if data.expires_in > time():
                self.redis.set(self.section_key(data.section, data.key), data.value,
                               ex=time()-data.expires_in)
                return True
        else:
            self.redis.set(self.section_key(
                data.section, data.key), data.value)
            return True

        return False

    def _delete_value(self, data: CacheData) -> bool:
        self.redis.delete(self.section_key(data.section, data.key))
        return True

    def purge_expired(self) -> int:
        return 0

    @staticmethod
    def section_key(section, key) -> str:
        return ('_' if not section else str(section))+':' +\
            ('_' if not key else str(key))
