from aiohttp import web
from modules.app import App
from modules.last import LastFM
from modules.spotify import Spotify
from modules.bot import Bot

__all__ = 'WebApp'

SONGS_COUNT = 5


class WebApp(App):
    def __init__(self, config_name: str = None):
        super().__init__(config_name)
        self.app = web.Application()
        self.__set_rotes()

        self.last = LastFM()
        self.spotify = Spotify()
        self.bot = Bot()

    def __set_rotes(self):
        self.app.router.add_post('/', self.handler)

    async def handler(self, request):
        request_content = await request.json()
        print('\n', request_content['update_id'], request_content['message']['text'], '\n')

        try:
            count_years = int(request_content['message']['text'])
        except:
            count_years = 3

        time_frame = self.last.get_timeframe(count_years)
        user_stat = await self.last.get_user_stat(time_frame)

        for i, track in enumerate(user_stat[:SONGS_COUNT]):
            artist = track['artist']['#text']
            title = track['name']

            mp3_url, image_url = await self.spotify.get_track_info(artist, title)

            if mp3_url:

                data = await request.json()
                message_text = f'{artist} - {title} {mp3_url}'
                await self.bot.send_message(data['message']['chat']['id'], message_text)

        return web.Response(status=200)