from typing import Optional, Dict, Union
import requests
from requests import HTTPError


class ApiFetcher:

    def __init__(self, base_url: str, **kwargs):
        self._base_url: str = base_url

    def _build_url(self, query_params: Dict, uri: str = '') -> str:
        url: str = self._base_url + uri + '?'
        query_params_quantity: int = len(query_params)

        if query_params_quantity > 0:
            for enum, key in enumerate(query_params):
                url += key + '=' + str(query_params[key])
                if enum < query_params_quantity - 1:
                    url += '&'

        return url

    def get_json(self, uri: str, **kwargs) -> Dict['str', Union[str, float]]:
        full_url = self._build_url(kwargs, uri=uri)
        resp = requests.get(full_url)
        if resp.status_code != 200:
            raise HTTPError('Error', resp.status_code, sep=':')
        return resp.json()

    @property
    def base_url(self):
        return self.base_url
