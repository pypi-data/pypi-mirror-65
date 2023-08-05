import unittest
from cache_gs.cache_classes.redis_setup import RedisSetup


class TestRedisSetup(unittest.TestCase):

    def test_init(self):

        rs = RedisSetup(
            'redis://localhost:6379?username=abcd&password=1234'
            '&client_name=me&encoding=utf-8&encoding_errors=strict&charset=utf-8'
            '&db=0&health_check_interval=10')

        self.assertIsInstance(rs, RedisSetup)

        rs = RedisSetup('redis://localhost:6379')
        self.assertIsInstance(rs, RedisSetup)

    def test_init_error(self):
        with self.assertRaises(Exception):
            RedisSetup('')

        with self.assertRaises(Exception):
            RedisSetup('redis://localhost:70000')

        with self.assertRaises(Exception):
            RedisSetup('redis://localhost:1234&db=a')
