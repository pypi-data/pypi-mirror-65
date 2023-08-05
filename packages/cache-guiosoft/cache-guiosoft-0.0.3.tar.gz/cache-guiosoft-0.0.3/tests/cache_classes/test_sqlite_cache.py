import os
import unittest
from unittest.mock import patch

from cache_gs.cache_classes.sqlite_cache import SQLiteCache
from tests.test_tools import raise_test_exception


class TestSQLiteCache(unittest.TestCase):

    def setUp(self):
        
        self.cache = SQLiteCache('sqlite://.cache')

    def tearDown(self):
        if os.path.isfile('.cache'):
            os.unlink('.cache')

    def test_sqlite(self):
        self.assertIsInstance(self.cache, SQLiteCache)

    def test_expired(self):
        self.cache.set_value('testing', 'expired', 'value', 100)
        x = self.cache.get_value('testing', 'expired')
        self.assertIsNone(x)

    def test_unexistent(self):
        x = self.cache.get_value('testing', 'unexistent_value', 'x')
        self.assertEqual(x, 'x')

    def test_delete(self):
        self.cache.set_value('testing', 'real_data', '1234')
        self.assertEqual(self.cache.get_value('testing', 'real_data'), '1234')
        self.cache.delete_value('testing', 'real_data')
        self.assertIsNone(self.cache.get_value('testing', 'real_data'))

    def test_purge(self):
        self.cache.set_value('testing', 'real_data', '1234', 100)
        self.assertGreater(self.cache.purge_expired(), 0)

    @patch("cache_gs.cache_classes.sqlite_cache.SuperCache.log_debug", lambda *args: raise_test_exception())
    def test_exception_setup(self):
        with self.assertRaises(Exception):
            SQLiteCache('sqlite://.cache')

    def test_get_value_exception(self):
        self.cache.conn = None
        self.assertFalse(self.cache.get_value("a", "b"))

    def test_set_value_exception(self):
        self.cache.conn = None
        self.assertFalse(self.cache.set_value("a", "b", '0'))

    def test_delete_value_exception(self):
        self.cache.conn = None
        self.assertFalse(self.cache.delete_value("a", "b"))

    def test_purge_exception(self):
        self.cache.conn = None
        self.assertEqual(self.cache.purge_expired(), 0)
