import os
import time
import requests
from typing import Dict

from model.team import Team
from core.configs import settings

class FootballAPIClient:
    _BASE_URL: str = 'https://api.football-data.org/v4'
    _FOOTBALL_API_TOKEN: str = settings.FOOTBALL_API_TOKEN
    _CACHE_TIMEOUT = settings.CACHE_TIMEOUT
    _cache: Dict[str, tuple] = {}

    def _request(self, path: str) -> Team:
        url = f'{self._BASE_URL}{path}'
        headers = { 'X-Auth-Token': self._FOOTBALL_API_TOKEN }

        # check cache
        if path in self._cache:
            cached_time, cached_response = self._cache[path]
            if time.time() - cached_time < self._CACHE_TIMEOUT:
                print(f'Load from cache path {path}')
                return cached_response

        print(f'No cache for path {path}, creating')
        response = requests.get(url, headers = headers)
        response.raise_for_status()
        data = Team.model_validate(response.json())

        # save on cache
        self._cache[path] = (time.time(), data)
        return data

    def get_team(self, id: int) -> Team:
        return self._request(f'/teams/{id}')