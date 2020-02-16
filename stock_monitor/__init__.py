from typing import Dict, Union, List

import requests
from datetime import date
from .api import ApiFetcher
from .time_module import get_last_n_days

# Type Variable to TimeSeriesDaily
TimeSeriesDaily = Dict[str, Dict[str, str]]


class AlphaVantageClient:

    def __init__(self, key: str, base_url: str = 'https://www.alphavantage.co'):
        self.base_url = base_url
        self.api_key = key
        self._alpha_vantage_api = ApiFetcher(base_url=base_url, key=key)

    def _limit_results(self, time_series: TimeSeriesDaily, past_limit_days: int) -> TimeSeriesDaily:
        limited_result: TimeSeriesDaily = {}

        last_LIMIT_days = get_last_n_days(past_limit_days)

        for day in last_LIMIT_days:
            str_day: str = str(day)
            if str_day in time_series.keys():
                limited_result[str_day] = time_series[str_day]

        return limited_result

    def get_time_series_daily(self, ticker: str, since_n_day_ago: int = 7) -> TimeSeriesDaily:
        try:
            data: Dict = self._alpha_vantage_api.get_json(
                uri='/query',
                function='TIME_SERIES_DAILY',
                symbol=ticker,
                datatype='json',
                outputsize='compact' if since_n_day_ago <= 100 else 'full',
                apikey=self.api_key
            )
        except requests.ConnectionError as e:
            raise requests.ConnectionError('You may not have internet connection', e, sep='\n')

        return self._limit_results(data['Time Series (Daily)'], since_n_day_ago)
