import unittest
from cache_gs.interfaces.super_cache import SuperCache
from unittest.mock import patch, Mock


class TestSuperCache(unittest.TestCase):

    def test_init(self):
        with self.assertRaises(Exception):
            SuperCache(None)

        with self.assertRaises(Exception):
            SuperCache('test')

    @patch("cache_gs.interfaces.super_cache.SuperCache.setup", Mock())
    def test_get_set_delete(self):
        sc = SuperCache('x')
        with self.assertRaises(Exception):
            sc._get_value('x', 'y')
        with self.assertRaises(Exception):
            sc._set_value(None)
        with self.assertRaises(Exception):
            sc._delete_value(None)
        with self.assertRaises(Exception):
            sc.purge_expired()

    @patch("cache_gs.interfaces.super_cache.SuperCache.setup", Mock())
    @patch("cache_gs.interfaces.super_cache.SuperCache._get_value", Mock())
    def test_get_value(self):
        SuperCache._get_value.return_value = None
        sc = SuperCache('x')
        self.assertEqual(sc.get_value('', '', 'default'), 'default')

        SuperCache._get_value.return_value = MockData()
        self.assertEqual(sc.get_value('', '', 'value'), 'value')

    @patch("cache_gs.interfaces.super_cache.SuperCache.setup", Mock())
    def test_delete(self):
        sc = SuperCache('x')
        with self.assertRaises(Exception):
            sc.delete_value('x', 'x')

    def test_logs(self):
        SuperCache.log_debug('TEST DEBUG')
        SuperCache.log_info('TEST_INFO')
    

class MockData:

    expired = False
    value = 'value'
