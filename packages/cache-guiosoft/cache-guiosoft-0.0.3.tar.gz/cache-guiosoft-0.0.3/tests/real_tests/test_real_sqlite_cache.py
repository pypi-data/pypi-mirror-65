import os
import unittest

from cache_gs import CacheGS
from cache_gs.utils.filesystem import remove_tree


class TestRealSQLiteCache(unittest.TestCase):

    def setUp(self):
        self.cache_file = '.cache'
        if not os.path.isdir(self.cache_file):
            os.mkdir(self.cache_file)

        self.cache = CacheGS('sqlite://' + self.cache_file)

    def tearDown(self):
        del (self.cache)
        remove_tree(self.cache_file)

    def test_init(self):
        self.assertIsInstance(self.cache, CacheGS)

    def test_get_set_delete(self):
        self.assertTrue(self.cache.set_value(
            'sec', 'key', '1234', expires_in=100000))
        value = self.cache.get_value('sec', 'key')
        self.assertEqual(value, '1234')
        self.assertTrue(self.cache.delete_value('sec', 'key'))

    def test_purge(self):
        self.assertTrue(self.cache.set_value('sec', 'key', '1234', 100))
        self.assertGreater(self.cache.purge_expired(), 0)
