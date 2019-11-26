import json

import requests
from aiohttp import ClientSession
from aiohttp import web

from modules.app import App


class Bot(App):
    def __init__(self):
        super().__init__()
        self.token = self.config['telegram_token']
        self.api_url = f'https://api.telegram.org/bot{self.token}/'

    def set_webhook(self):
        url = self.api_url + 'setWebhook'
        data = {
            'url': self.config['webhook_url']
        }

        resp = requests.post(url, data).json()

    async def send_message(self, chat_id, text):
        headers = {
            'Content-Type': 'application/json'
        }
        message = {
            'chat_id': chat_id,
            'text': text
        }

        async with ClientSession() as session:

            async with session.post(self.api_url + 'sendMessage',
                                    data=json.dumps(message),
                                    headers=headers) as resp:

                assert resp.status == 200

                try:
                    assert resp.status == 200
                except AssertionError:
                    return web.Response(status=500)


if __name__ == '__main__':
    bot = Bot()
    bot.set_webhook()
