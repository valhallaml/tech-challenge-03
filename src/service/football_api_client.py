import os
import time
import requests
from typing import Dict

from model.team import Team
from model.matches import Matches
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
        data = response.json()

        # save on cache
        self._cache[path] = (time.time(), data)
        return data

    def get_team(self, id: int) -> Team:
        json = self._request(f'/teams/{id}')
        return Team.model_validate(json)
    
    def get_matches(self) -> Matches:
        '''Brasileirão de 2024'''
        json = self._request('/competitions/2013/matches?season=2024&status=FINISHED')
        return Matches.model_validate(json) 