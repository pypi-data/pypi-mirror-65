from unittest.mock import Mock, patch
import unittest
from cache_gs.cache_classes.redis_cache import RedisCache
import redis
from time import time


class TestRedisCache(unittest.TestCase):

    @patch("redis.Redis", Mock())
    def test_init(self):
        rc = RedisCache('redis://localhost:6379')
        self.assertIsInstance(rc, RedisCache)
        self.assertEqual(rc.purge_expired(), 0)

    @patch("redis.Redis", Mock())
    def test_get_set(self):
        rc = RedisCache('redis://localhost:6379')
        rc.redis.get = lambda *args: b"abc"
        self.assertEqual(rc.get_value("sec", "key"), "abc")
        rc.redis.get = lambda *args: None
        self.assertIsNone(rc.get_value("sec", "key"))

        rc.redis.set = lambda *args, **kwargs: None
        self.assertTrue(rc.set_value("sec", "key", "abc"))
        self.assertFalse(rc.set_value("sec", "key", "abc", 10))
        self.assertTrue(rc.set_value("sec", "key", "abc", time()+10))

        rc.redis.delete = lambda *args, **kwargs: True
        self.assertTrue(rc.delete_value("sec", "key"))
