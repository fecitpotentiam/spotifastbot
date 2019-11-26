from typing import Tuple

import spotipy
import spotipy.util as util
from aiohttp import ClientSession

from modules.app import App


class Spotify(App):
    def __init__(self):
        super().__init__()
        self.token = self.__get_token()
        self.app = spotipy.Spotify(auth=self.token)

    def __get_token(self):
        return util.prompt_for_user_token(self.config['spotify_username'],
                                          self.config['spotify_scope'],
                                          client_id=self.config['spotify_client_id'],
                                          client_secret=self.config['spotify_client_secret'],
                                          redirect_uri=self.config['spotify_redirect_url'])

    async def __get_track(self, artist, title) -> dict or None:
        url = 'https://api.spotify.com/v1/search'
        params = {
            'q': f'{artist}:{title}',
            'type': 'artist,track'
        }

        header = {'Authorization': 'Bearer ' + self.token}

        async with ClientSession() as session:
            async with session.get(url, params=params, headers=header) as response:
                response = await response.json()
        try:
            return response['tracks']['items'][0]
        except IndexError or KeyError:
            return None

    async def get_track_info(self, artist, title) -> Tuple[str, str] or Tuple[None, None]:
        track = await self.__get_track(artist, title)
        if track:
            mp3_url = track['preview_url']
            image_url = track['album']['images'][0]['url']

            return mp3_url, image_url
        else:
            return None, None
