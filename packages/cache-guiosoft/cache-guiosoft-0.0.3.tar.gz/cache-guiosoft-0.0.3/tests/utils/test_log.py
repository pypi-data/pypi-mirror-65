import unittest
from cache_gs.utils.logging import get_logger


class TestLog(unittest.TestCase):

    def test_log(self):
        with self.assertLogs('cache_gs', level='INFO'):
            logger = get_logger()
            logger.info('TESTING INFO')
            logger.debug('TESTING DEBUG')
