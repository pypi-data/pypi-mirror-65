import os
import time
import unittest

from cache_gs import CacheGS
from cache_gs.cache_classes.file_cache import FileCache
from cache_gs.utils.filesystem import remove_tree


class TestFileCache(unittest.TestCase):

    def setUp(self):
        self.cache_folder = '.cache'
        self.file_cache = CacheGS('path://'+self.cache_folder)

    def tearDown(self):
        if os.path.isdir(self.cache_folder):
            remove_tree(self.cache_folder)

    def test_setup_error_folder(self):
        with self.assertRaises(Exception):
            FileCache('path://.cache_/error')

    def test_purge(self):
        self.assertTrue(self.file_cache.set_value(
            'test', 'key', 'abcd', time.time()+1))
        time.sleep(1)
        self.assertTrue(self.file_cache.purge_expired() > 0)

    def test_get_default(self):
        self.assertEqual(self.file_cache.get_value(
            'test', 'key_', 'abcd'), 'abcd')
