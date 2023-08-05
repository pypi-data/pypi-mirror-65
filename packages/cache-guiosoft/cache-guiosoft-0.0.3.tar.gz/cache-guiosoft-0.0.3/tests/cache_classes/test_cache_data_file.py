import datetime
import os
import unittest
from unittest.mock import Mock, patch

from cache_gs.cache_classes.cache_data_file import CacheData, CacheDataFile
from tests.test_tools import raise_test_exception


class TestCacheDataFile(unittest.TestCase):

    def setUp(self):
        self.file_name = 'test.json'

    def tearDown(self):
        if os.path.isfile(self.file_name):
            os.unlink(self.file_name)

    def test_save(self):
        cd = CacheData("test_section", "test_key", "test_value", 0)
        cdf = CacheDataFile('test', cd)
        self.assertTrue(cdf.save(self.file_name))

        cdf2 = CacheDataFile(self.file_name)
        self.assertEqual(cdf.data, cdf2.data)

        cd2 = CacheData("test_section", "test_key",
                        "test_value_", 0, datetime.datetime.now())
        self.assertNotEqual(cd, cd2)

        self.assertNotEqual(cd, None)

    def test_cache_data(self):
        cd = CacheData('sec', 'key', 'value', 0)
        self.assertEqual(repr(cd), "CacheData('sec','key','value',0)")

    def test_repr(self):
        cd = CacheData('sec', 'key', 'value', 0)
        cdf = CacheDataFile('test', cd)
        self.assertEqual(
            repr(cdf), "CacheDataFile('test',CacheData('sec','key','value',0))")

    @patch("os.path.isfile", Mock())
    def test_load_exception(self):
        os.path.isfile.return_value = True
        cdf = CacheDataFile()
        self.assertFalse(cdf.load('abcd'))

    @patch("json.dumps", lambda **kwargs: raise_test_exception())
    def test_save_exception(self):
        cd = CacheData("sec", "key", "value", 0)
        cdf = CacheDataFile(cache_data=cd)
        self.assertFalse(cdf.save('abcd'))
        if os.path.isfile('abcd'):
            os.unlink('abcd')
