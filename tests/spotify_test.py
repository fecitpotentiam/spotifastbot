import asyncio
import unittest

from modules.spotify import Spotify


class TestSpotify(unittest.TestCase):
    def setUp(self):
        self.spotify = Spotify()

    def test_get_track_info(self):
        mp3_url, image_url = asyncio.get_event_loop().run_until_complete(
                             self.spotify.get_track_info('System Of A Down', 'Toxicity'))

        self.assertEqual(mp3_url, 'https://p.scdn.co/mp3-preview/cd2a1f9fd7619bdae4e2e718b1'
                                  '1d5bb054a3d677?cid=84e7533c976b4f3688075bf1988630c7')
        self.assertEqual(image_url, 'https://i.scdn.co/image/ab67616d0000b27330d45198d0c9e8841f9a9578')
