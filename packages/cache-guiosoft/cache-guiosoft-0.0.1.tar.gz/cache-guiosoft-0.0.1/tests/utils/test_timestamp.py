import unittest
from cache_gs.utils.timestamp import base64_to_int, int_to_base64, section_key_hash


class TestTimeStamp(unittest.TestCase):

    def test_base64(self):
        b = int_to_base64(10)
        i = base64_to_int(b)

        self.assertEqual(10, i)

    def test_lenght(self):
        i = 1
        l = len(int_to_base64(0))
        igual = True
        last = 2**32
        while i <= last and igual:
            igual = len(int_to_base64(i)) == l
            i *= 2

        self.assertTrue(igual)

    def test_section_key_hash(self):
        hash = section_key_hash('section', 'key')
        self.assertIsNotNone(hash)
