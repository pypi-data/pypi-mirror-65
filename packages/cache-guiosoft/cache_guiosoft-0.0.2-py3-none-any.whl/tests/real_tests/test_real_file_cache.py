import os
import unittest

from cache_gs import CacheGS
from cache_gs.utils.filesystem import remove_tree


class TestRealFileCache(unittest.TestCase):

    def setUp(self):
        self.cache_path = ".cache_dir"
        self.cache = CacheGS('path://'+self.cache_path)

    def tearDown(self):
        if os.path.isdir(self.cache_path):
            remove_tree(self.cache_path)

    def test_file_cache(self):
        self.assertIsInstance(self.cache, CacheGS)

    def test_get_set_delete(self):
        self.assertTrue(self.cache.set_value('sec', 'key', '1234'))
        self.assertEqual(self.cache.get_value('sec', 'key'), '1234')
        self.assertTrue(self.cache.delete_value('sec', 'key'))

    def test_purge(self):
        self.assertTrue(self.cache.set_value('sec', 'key', '1234', 100))
        self.assertGreater(self.cache.purge_expired(), 0)
