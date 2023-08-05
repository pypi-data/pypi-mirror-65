import unittest

from cache_gs import CacheGS


class TestCacheGS(unittest.TestCase):

    def test_init_fail(self):
        with self.assertRaises(Exception):
            CacheGS('error')
