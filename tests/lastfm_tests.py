import asyncio
import unittest

from modules.last import LastFM


class TestLastFM(unittest.TestCase):
    def setUp(self):
        self.last = LastFM()

    def test_get_user_stat(self):
        user_stat = asyncio.get_event_loop().run_until_complete(
                             self.last.get_user_stat(3))

        self.assertIsInstance(user_stat, list)
