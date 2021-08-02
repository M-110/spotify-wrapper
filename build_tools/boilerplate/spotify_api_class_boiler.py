import json
from typing import List, Union, Optional

import requests

from .authentication.authorization_code_flow_pkce import PKCE
from .object_library import SpotifyObject, AlbumObject, ErrorObject, \
    PagingObject, SimplifiedTrackObject, ArtistObject, TrackObject, \
    SimplifiedAlbumObject, CategoryObject, SimplifiedPlaylistObject, \
    RecommendationsObject, EpisodeObject, SavedAlbumObject, ImageObject, \
    SimplifiedShowObject, SimplifiedEpisodeObject, AudioFeaturesObject, \
    SavedShowObject, SavedEpisodeObject, SavedTrackObject, PlayHistoryObject, \
    PlaylistObject, ShowObject, AudioAnalysisObject, UserObject
from .utilities import requires, CustomResponse


class SpotifyAPI:
    """Hello World!"""
    HTTP_METHODS = {
        'POST': requests.post,
        'GET': requests.get,
        'PUT': requests.put
    }

    _headers = {'Accept': ''}

    def __init__(self):
        self._flow = PKCE()
        self._credentials: dict = self._flow.get_credentials()
        self._access_token: str = self._credentials['access_token']
        self._scopes: str = self._credentials['scope']
        self._headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self._access_token}'
        }

    @property
    def credentials(self):
        """Return the credentials TODO: Explain"""
        return self._credentials

    @property
    def access_token(self):
        """Return the access_token TODO: Explain"""
        return self._access_token

    @property
    def scopes(self):
        """Return the scopes TODO: Explain"""
        return self._scopes

    @property
    def headers(self):
        """Return the headers TODO: Explain"""
        return self._headers

    # TODO: Add type hints
    def _get(self, url, query_params, json_body):
        params = self._convert_query_params(query_params)
        print(f'{url=}')
        print(f'{params=}')
        print(f'{json_body=}')
        try:
            response = requests.get(url, params=params, headers=self.headers)
            error = 'error' in response.text[:10]
            print(f'URL requested: {response.request.url!r}')
        except ConnectionError as e:
            response = CustomResponse(
                '{ "error": { "status": "ConnectionError", "message": "' +
                str(e) + '"}}')
            error = True
        if error:
            response = json.loads(response.text)['error']
        return response, error

    def _put(self, endpoint):
        return requests.put(endpoint, headers=self.headers)

    def _post(self, endpoint):
        return requests.post(endpoint, headers=self.headers)

    # TODO: Extract as function
    def _convert_query_params(self, params: dict):
        """Remove unused parameters and convert lists to comma separated
        strings. """
        params = {
            key: value for key, value in params.items() if value is not None
        }
        for key, value in params.items():
            if isinstance(value, list):
                params[key] = ','.join(value)
        return params

    # TODO: Extract as function
    def _convert_array_to_list(self, response,
                               type_) -> List[Optional[SpotifyObject]]:
        """Convert the json dictionary array into a list."""
        json_dict = json.loads(response)
        if isinstance(json_dict, list):
            array = json_dict
        else:
            array = list(json_dict.values())[0]
        return [type_(value) if value is not None else None for value in array]
