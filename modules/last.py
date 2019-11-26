import datetime
import logging
import time
from datetime import timedelta
from typing import Tuple, List

from aiohttp import ClientSession

from .app import App

YEAR = 365
DAYS_DELTA = 7


class LastFM(App):
    """
    Using LastFM API to get user's statistic
    """
    def __init__(self, config=None):
        super().__init__(config)

    @staticmethod
    def __get_timeframe(count_years: int = 3) -> Tuple[str, str]:
        """
        Get one week period a few years ago (specified with count years)
        :param count_years: time delta
        :return: first_date_unixtime (upper limit of the range)
                 second_date_unixtime (lower limit of the range)
        """
        first_date = datetime.datetime.now() - timedelta(days=YEAR * count_years)
        second_date = first_date + timedelta(days=DAYS_DELTA)

        first_date_unixtime = str(int(time.mktime(first_date.timetuple())))
        second_date_unixtime = str(int(time.mktime(second_date.timetuple())))

        return first_date_unixtime, second_date_unixtime

    async def get_user_stat(self, count_years: int) -> List[dict]:
        """
        Get user's top weekly tracks in period
        :param count_years: time delta
        :return: list with top user's tracks
        """
        timeframe = self.__get_timeframe(count_years)
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
