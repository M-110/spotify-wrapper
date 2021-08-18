import json
from urllib.parse import urlencode
from typing import List, Tuple, Union, Optional

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

QUERY_DICT = {'albums': SimplifiedAlbumObject,
              'artists': ArtistObject,
              'playlists': PlaylistObject,
              'tracks': TrackObject,
              'shows': SimplifiedShowObject,
              'episodes': SimplifiedEpisodeObject}


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
    def _get(self, url, query_params, json_body) -> Tuple[dict, bool]:
        params = self._convert_query_params(query_params)
        print('-----------------get---------------------')
        print(f'{url=}')
        print(f'{params=}')
        print(f'{json_body=}')
        try:
            response = requests.get(url, params=params, headers=self.headers)
            error = 'error' in response.text[:10]
            print(f'URL requested: {response.request.url!r}')
        except ConnectionError as e:
            # TODO: This seems weird?
            response = CustomResponse(
                '{ "error": { "status": "ConnectionError", "message": "' +
                str(e) + '"}}')
            error = True
        if response.status_code == 204:
            response = CustomResponse(
                '{ "error": { "status": "204 No Content", "message": "' +
                'The server successfully responded but didn\'t return '
                'any content"}}')
            error = True
        if error:
            response = json.loads(response.text)['error']
        else:
            response = json.loads(response.text)
        print(f'get returns type: {type(response)}')
        print('----------------ENDget--------------------')
        return response, error

    def _put(self, endpoint):
        return requests.put(endpoint, headers=self.headers)

    def _post(self, endpoint):
        return requests.post(endpoint, headers=self.headers)

    @staticmethod
    def _convert_query_params(params: dict):
        """Remove unused parameters and convert lists to comma separated
        strings. """
        params = {
            key: value for key, value in params.items() if value is not None
        }
        for key, value in params.items():
            if isinstance(value, list):
                params[key] = ','.join(value)
        return params

    @staticmethod
    def _convert_array_to_list(response,
                               type_) -> List[Optional[SpotifyObject]]:
        """Convert the json dictionary array into a list."""
        if isinstance(response, list):
            array = response
        else:
            array = list(response.values())[0]
        return [type_(value) if value is not None else None for value in array]

    def search_for_an_item(
            self,
            q: str,
            type_: List[str],
            market: str = None,
            limit: int = None,
            offset: int = None,
            include_external: str = None
    ) -> Union[List[PagingObject[Union[ArtistObject, SimplifiedAlbumObject,
                                       SimplifiedPlaylistObject,
                                       TrackObject, SimplifiedShowObject,
                                       SimplifiedEpisodeObject]]],
               ErrorObject]:
        """
        Get Spotify Catalog information about albums, artists, playlists,
        tracks, shows or episodes that match a keyword string.

        Args:
            q: Search query keywords and optional field filters and operators
            type_: A list of strings of the item types to search across. Valid
                types are: 'album', 'artist', 'playlist', 'track', 'show' and
                'episode'.
            market: Optional; An ISO 3166-1 alpha-2 country code or the string
                'from_token'.
            limit: Optional; Maximum number of results to return. Default: 20.
                Minimum: 1. Maximum: 50. Note: The limit is applied within each
                type, not the total response. For example, if the limit value
                is 3 and the type is ['artist', 'album'], the response contains
                3 artists and 3 albums.
            offset: Optional; The index of the first result to return. Default:
                0. Maximum: 1,000. Use with limit to get the next page of
                search results.
            include_external: Optional; Possible values: 'audio'. If 'audio' is
                specified the response will include any relevant audio content
                that is hosted externally. By default external content is
                filtered out from responses.
        """

        url = f'https://api.spotify.com/v1/search?'
        path_params = dict(q=q, type=','.join(type_), market=market,
                           limit=limit, offset=offset,
                           include_external=include_external)
        active_path_params = {key: value for key, value in path_params.items()
                              if value is not None}
        url += urlencode(active_path_params)
        query_params = {}
        json_body = {}
        response, error = self._get(url, query_params, json_body)
        if error:
            return ErrorObject(response)
        return [PagingObject(value, QUERY_DICT[key]) for key, value in
                response.items()]

