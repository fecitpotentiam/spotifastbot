import json

import requests
from aiohttp import ClientSession
from aiohttp import web

from .app import App


class Bot(App):
    """
    Simple Telegram bot
    """
    def __init__(self, config=None):
        super().__init__(config)
        self.token = self.config['telegram_token']
        self.api_url = f'https://api.telegram.org/bot{self.token}/'

    def set_webhook(self):
        """
        Set url to receive events from Telegram (uses webhook-url from configuration file)
        :return: None
        """
        url = self.api_url + 'setWebhook'
        data = {
            'url': self.config['webhook_url']
        }

        resp = requests.post(url, data).json()

        if resp['ok']:
            print('Webhook is installed')
        else:
            print('Webhook is not installed. Please check your settings.')

    async def send_message(self, chat_id: int, text: str) -> web.Response:
        """

        :param chat_id: user's telegram_id
        :param text: message_text
        :return: web.Response: response with status
        """
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

        return web.Response(status=200)


if __name__ == '__main__':
    bot = Bot()
    bot.set_webhook()
