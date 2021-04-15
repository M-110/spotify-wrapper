import json

import requests
from typing import Optional, List, Union
from .authorization_flow.server_pkce_flow import get_new_credentials
from .object_library import AlbumObject, ErrorObject, SpotifyObject
from .utilities import requires


# from object_index import AlbumObject


class SpotifyAPI:
    HTTP_METHODS = {'POST': requests.post,
                    'GET': requests.get,
                    'PUT': requests.put}

    def __init__(self):
        self._credentials: dict = get_new_credentials()
        self._access_token: str = self._credentials['access_token']
        self._scopes: str = self._credentials['scope']
        self._headers = {'Accept': 'application/json',
                         'Content-Type': 'application/json',
                         'Authorization': f'Bearer {self._access_token}'}

    @property
    def credentials(self):
        return self._credentials

    @property
    def access_token(self):
        return self._access_token

    @property
    def scopes(self):
        return self._scopes

    @property
    def headers(self):
        return self._headers

    def _get(self, url, query_params, json_body):
        params = self._convert_query_params(query_params)
        print(f'{url=}')
        print(f'{params=}')
        print(f'{json_body=}')
        response = requests.get(url, params=params, headers=self.headers)
        error = 'error' in response.text[:10]
        print(f'URL requested: {response.request.url!r}')
        return response, error

    def _put(self, endpoint):
        return requests.put(endpoint, headers=self.headers)

    def _post(self, endpoint):
        return requests.post(endpoint, headers=self.headers)
    
    def _convert_query_params(self, params: dict):
        """Remove unused parameters and convert lists to comma separated strings."""
        params = {key: value for key, value in params.items() if value is not None}
        for key, value in params.items():
            if isinstance(value, list):
                params[key] = ','.join(value)
        return params

    def _convert_array_to_list(self, response, type_) -> List[Optional[SpotifyObject]]:
        """Convert the json dictionary array into a list."""
        json_dict = json.loads(response)
        array = list(json_dict.values())[0]
        return [type_(value) if value is not None else None
                for value in array]

    @requires(['user-read-email', 'user-read-private'])
    def get_current_users_profile(self):
        return self._get('https://api.spotify.com/v1/me')

    @requires(['user-modify-playback-state'])
    def play_next_song(self):
        return self._post('https://api.spotify.com/v1/me/player/next')

    def get_multiple_albums(self, ids: List[str], market: str = None) -> Union[List[Optional[AlbumObject]], ErrorObject]:
        """
        Get Spotify catalog information for multiple albums identified by their
    Spotify IDs.

    Args:
        ids: A list of strings of the Spotify IDs for the albums. Maximum: 20
          IDs.
        market: Optional; An ISO 3166-1 alpha-2 country code or the string
          'from_token'.
        """
        url = f'https://api.spotify.com/v1/albums'
        query_params = {'ids': ids, 'market': market}
        json_body = {}
        response, error = self._get(url, query_params, json_body)
        if error:
            return ErrorObject(response.text)
        return self._convert_array_to_list(response.text, AlbumObject)
