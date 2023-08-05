import unittest
from cache_gs.utils.types import str_to_type, type_to_str


class TestTypes(unittest.TestCase):

    def test_str_to_type(self):
        self.assertIsNotNone(str_to_type('int'))
        self.assertIsNone(str_to_type('None'))

    def test_type_to_str(self):
        self.assertIsNotNone(type_to_str(int))
        with self.assertRaises(Exception):
            type_to_str(None)
