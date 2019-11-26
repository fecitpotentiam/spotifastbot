import datetime
import logging
import time
from datetime import timedelta
from typing import Tuple

from aiohttp import ClientSession

from modules.app import App

logger = logging.getLogger('aiohttp_test')
logger.setLevel(logging.DEBUG)

YEAR = 365
COUNT_YEARS = 2
DAYS_DELTA = 7


class LastFM(App):
    def __init__(self):
        super().__init__()

    @staticmethod
    def get_timeframe(count_years=3) -> Tuple[str, str]:
        first_date = datetime.datetime.now() - timedelta(days=YEAR * count_years)
        second_date = first_date + timedelta(days=DAYS_DELTA)

        first_date_unixtime = str(int(time.mktime(first_date.timetuple())))
        second_date_unixtime = str(int(time.mktime(second_date.timetuple())))

        return first_date_unixtime, second_date_unixtime

    async def get_user_stat(self, timeframe: Tuple[str, str]) -> dict:
        url = 'http://ws.audioscrobbler.com/2.0/'

        params = {
            'method': 'user.getweeklytrackchart',
            'user': self.config['last_username'],
            'api_key': self.config['last_api_key'],
            'format': 'json',
            'from': timeframe[0],
            'to': timeframe[1]
        }

        async with ClientSession() as session:
            async with session.get(url, params=params) as response:
                response = await response.json()

        return response['weeklytrackchart']['track']
