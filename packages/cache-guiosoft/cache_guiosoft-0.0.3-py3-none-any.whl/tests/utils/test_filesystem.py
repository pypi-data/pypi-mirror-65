import unittest
import os
from cache_gs.utils.filesystem import remove_tree


class TestFileSystem(unittest.TestCase):

    def setUp(self):
        self.path = '.cache'

    def test_remove_tree(self):
        files = [
            'file1.txt',
            'p1/file2.txt',
            'p2/file3.txt',
            'p1/pp1/file4.txt',
            'p1/pp1/file5.txt',
            'p2/pp2/file6.txt',
            'p2/pp2/file7.txt',
            'p3/pp3/ppp3/file8.txt'
        ]

        for file in files:
            filename = os.path.join(self.path, file)
            dirname = os.path.dirname(filename)
            if not os.path.isdir(dirname):
                os.makedirs(dirname)

            with open(filename, 'w') as f:
                f.write('test')

        remove_tree(self.path)
        self.assertFalse(os.path.isdir(self.path))
