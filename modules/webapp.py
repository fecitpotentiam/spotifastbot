from aiohttp import web, web_request
from .app import App
from .last import LastFM
from .spotify import Spotify
from .bot import Bot


SONGS_COUNT = 5


class WebApp(App):
    """
    Web Application with one route and webhook's handler
    """
    def __init__(self, config_name: str = None):
        super().__init__(config_name)
        self.app = web.Application()
        self.__set_routes()

        self.last = LastFM()
        self.spotify = Spotify()
        self.bot = Bot()

    def __set_routes(self):
        """
        Add route for webhook handler
        :return: None
        """
        self.app.router.add_post('/', self.handle_request)

    async def handle_request(self, request: web_request.Request) -> web.Response:
        """
        Handler for Telegram's requests
        :param request: request from Telegram's webhook
        :return: web.response: 200 response to Telegram
        """
        request_content = await request.json()
        print('\n', request_content['update_id'], request_content['message']['text'], '\n')

        try:
            count_years = int(request_content['message']['text'])
        except ValueError:
            count_years = 3

        user_stat = await self.last.get_user_stat(count_years)

        for i, track in enumerate(user_stat[:SONGS_COUNT]):
            artist = track['artist']['#text']
            title = track['name']

            mp3_url, image_url = await self.spotify.get_track_info(artist, title)

            if mp3_url:

                data = await request.json()
                message_text = f'{artist} - {title} {mp3_url}'
                await self.bot.send_message(data['message']['chat']['id'], message_text)

        return web.Response(status=200)
