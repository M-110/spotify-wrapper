import json

import requests
from requests.exceptions import ConnectionError
from typing import Optional, List, Union
from .authorization_flow.server_pkce_flow import get_new_credentials
from .object_library import AlbumObject, ErrorObject, SpotifyObject, PagingObject, TrackObject, SimplifiedTrackObject, \
    ArtistObject, SimplifiedAlbumObject, SimplifiedPlaylistObject, CategoryObject
from .utilities import requires, CustomResponse


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
        try:
            response = requests.get(url, params=params, headers=self.headers)
            error = 'error' in response.text[:10]
            print(f'URL requested: {response.request.url!r}')
        except ConnectionError as e:
            response = CustomResponse('{ "error": { "status": "ConnectionError",'
                                      ' "message": "' + str(e) + '"}}')
            error = True
        if error:
            response = json.loads(response.text)['error']
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

    def get_multiple_albums(self, ids: List[str], market: str = None) -> Union[
        List[Optional[AlbumObject]], ErrorObject]:
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
            return ErrorObject(response)
        return self._convert_array_to_list(response.text, AlbumObject)

    def get_an_album(self, id_: str, market: str = None) -> Union[Optional[AlbumObject], ErrorObject]:
        """
        Get Spotify catalog information for a single album.

    Args:
        id_: The Spotify ID of the album.
        market: Optional; An ISO 3166-1 alpha-2 country code or the string
          'from_token'.
        """
        url = f'https://api.spotify.com/v1/albums/{id_}'
        query_params = {'market': market}
        json_body = {}
        response, error = self._get(url, query_params, json_body)
        if error:
            return ErrorObject(response.text)
        return AlbumObject(response.text)
    
    def get_an_albums_tracks(self, id_: str, market: str = None, limit: int = None, offset: int = None) -> Union[PagingObject[SimplifiedTrackObject], ErrorObject]:
        """
        Get Spotify catalog information about an album’s tracks. Optional
    parameters can be used to limit the number of tracks returned.

    Args:
        id_: The Spotify ID of the album.
        market: Optional; An ISO 3166-1 alpha-2 country code or the string
          'from_token'.
        limit: Optional; The maximum number of tracks to return.  Default: 20.
          Minimum: 1. Maximum: 50.
        offset: Optional; The index of the first track to return. Default: 0.
        """
        url = f'https://api.spotify.com/v1/albums/{id_}/tracks'
        query_params = {'market': market, 'limit': limit, 'offset': offset}
        json_body = {}
        response, error = self._get(url, query_params, json_body)
        if error:
            return ErrorObject(response)
        return PagingObject(response.text, SimplifiedTrackObject)
    
    def get_multiple_artists(self, ids: List[str]) -> List[Optional[ArtistObject]]:
        """
        Get Spotify catalog information for several artists based on their Spotify
    IDs.

    Args:
        ids: A list of strings of the Spotify IDs for the artists. Maximum: 50
          IDs.
        """
        url = f'https://api.spotify.com/v1/artists'
        query_params = {'ids': ids}
        json_body = {}
        response, error = self._get(url, query_params, json_body)
        if error:
            return ErrorObject(response)
        return self._convert_array_to_list(response.text, ArtistObject)
    
    def get_an_artist(self, id_: str) -> Union[ArtistObject, ErrorObject]:
        """
        Get Spotify catalog information for a single artist identified by their
    unique Spotify ID.

    Args:
        id_: The Spotify ID of the artist.
        """
        url = f'https://api.spotify.com/v1/artists/{id_}'
        query_params = {}
        json_body = {}
        response, error = self._get(url, query_params, json_body)
        if error:
            return ErrorObject(response)
        return ArtistObject(response.text)
    
    def get_an_artists_top_tracks(self, id_: str, market: str) -> Union[List[TrackObject], ErrorObject]:
        """
        Get Spotify catalog information about an artist’s top tracks by country.

    Args:
        id_: The Spotify ID of the artist.
        market: An ISO 3166-1 alpha-2 country code or the string 'from_token'.
        """
        url = f'https://api.spotify.com/v1/artists/{id_}/top-tracks'
        query_params = {'market': market}
        json_body = {}
        response, error = self._get(url, query_params, json_body)
        if error:
            return ErrorObject(response)
        return self._convert_array_to_list(response.text, TrackObject)

    def get_an_artists_related_artists(self, id_: str) -> Union[List[ArtistObject], ErrorObject]:
        """
        Get Spotify catalog information about artists similar to a given artist.
    Similarity is based on analysis of the Spotify community’s listening
    history.

    Args:
        id_: The Spotify ID of the artist.
        """
        url = f'https://api.spotify.com/v1/artists/{id_}/related-artists'
        query_params = {}
        json_body = {}
        response, error = self._get(url, query_params, json_body)
        if error:
            return ErrorObject(response)
        return self._convert_array_to_list(response.text, ArtistObject)
    
    def get_an_artists_albums(self, id_: str, include_groups: List[str] = None, market: str = None, limit: int = None, offset: int = None) -> Union[PagingObject[SimplifiedAlbumObject], ErrorObject]:
        """
        Get Spotify catalog information about an artist’s albums.

    Args:
        id_: The Spotify ID of the artist.
        include_groups: Optional; A list of strings of the keywords that will
          be used to filter the response. If not supplied, all album types
          will be returned. Valid keywords are 'album', 'single',
          'appears_on', and 'compilation'.
        market: Optional; An ISO 3166-1 alpha-2 country code or the string
          'from_token'.
        limit: Optional; The maximum number of albums to return.  Default: 20.
          Minimum: 1. Maximum: 50.
        offset: Optional; The index of the first album to return. Default: 0.
        """
        url = f'https://api.spotify.com/v1/artists/{id_}/albums'
        query_params = {'include_groups': include_groups, 'market': market, 'limit': limit, 'offset': offset}
        json_body = {}
        response, error = self._get(url, query_params, json_body)
        if error:
            return ErrorObject(response)
        return PagingObject(response.text, SimplifiedAlbumObject)
    
    def get_all_new_releases(self, country: str = None, limit: int = None, offset: int = None) -> Union[PagingObject[SimplifiedAlbumObject], ErrorObject]:
        """
        Get a list of new album releases featured in Spotify (shown, for example,
    on a Spotify player’s “Browse” tab).

    Args:
        country: Optional; An ISO 3166-1 alpha-2 country code or the string
          'from_token'.
        limit: Optional; The maximum number of albums to return.  Default: 20.
          Minimum: 1. Maximum: 50.
        offset: Optional; The index of the first album to return. Default: 0.
        """
        url = f'https://api.spotify.com/v1/browse/new-releases'
        query_params = {'country': country, 'limit': limit, 'offset': offset}
        json_body = {}
        response, error = self._get(url, query_params, json_body)
        if error:
            return ErrorObject(response)
        return PagingObject(response.text, SimplifiedAlbumObject)

    def get_all_featured_playlists(self, country: str = None, locale: str = None, timestamp: str = None,
                                   limit: int = None, offset: int = None) -> Union[
        PagingObject[SimplifiedPlaylistObject], ErrorObject]:
        """
        Get a list of Spotify featured playlists (shown, for example, on a Spotify
    player’s ‘Browse’ tab).

    Args:
        country: Optional; An ISO 3166-1 alpha-2 country code or the string
          'from_token'.
        locale: Optional; The desired language, consisting of a lowercase ISO
          639-1 language code and an uppercase ISO 3166-1 alpha-2 country
          code, joined by an underscore. For example: es_MX, meaning “Spanish
          (Mexico)”. Provide this parameter if you want the results returned
          in a particular language (where available). Note that, if locale is
          not supplied, or if the specified language is not available, all
          strings will be returned in the Spotify default language (American
          English). The locale parameter, combined with the country parameter,
          may give odd results if not carefully matched.
        timestamp: Optional; A timestamp in ISO 8601 format: yyyy-MM-
          ddTHH:mm:ss. Use this parameter to specify the user’s local time to
          get results tailored for that specific date and time in the day. If
          not provided, the response defaults to the current UTC time.
          Example: “2014-10-23T09:00:00” for a user whose local time is 9AM.
          If there were no featured playlists (or there is no data) at the
          specified time, the response will revert to the current UTC time.
        limit: Optional; The maximum number of albums to return.  Default: 20.
          Minimum: 1. Maximum: 50.
        offset: Optional; The index of the first album to return. Default: 0.
        """
        url = f'https://api.spotify.com/v1/browse/featured-playlists'
        query_params = {'country': country, 'locale': locale, 'timestamp': timestamp, 'limit': limit, 'offset': offset}
        json_body = {}
        response, error = self._get(url, query_params, json_body)
        if error:
            return ErrorObject(response)
        return PagingObject(response.text, SimplifiedPlaylistObject)
    
    def get_all_categories(self, country: str = None, locale: str = None, timestamp: str = None, limit: int = None, offset: int = None) -> Union[PagingObject[CategoryObject], ErrorObject]:
        """
        Get a list of categories used to tag items in Spotify (on, for example,
    the Spotify player’s “Browse” tab).

    Args:
        country: Optional; An ISO 3166-1 alpha-2 country code or the string
          'from_token'.
        locale: Optional; The desired language, consisting of a lowercase ISO
          639-1 language code and an uppercase ISO 3166-1 alpha-2 country
          code, joined by an underscore. For example: es_MX, meaning “Spanish
          (Mexico)”. Provide this parameter if you want the results returned
          in a particular language (where available). Note that, if locale is
          not supplied, or if the specified language is not available, all
          strings will be returned in the Spotify default language (American
          English). The locale parameter, combined with the country parameter,
          may give odd results if not carefully matched.
        timestamp: Optional; A timestamp in ISO 8601 format: yyyy-MM-
          ddTHH:mm:ss. Use this parameter to specify the user’s local time to
          get results tailored for that specific date and time in the day. If
          not provided, the response defaults to the current UTC time.
          Example: “2014-10-23T09:00:00” for a user whose local time is 9AM.
          If there were no featured playlists (or there is no data) at the
          specified time, the response will revert to the current UTC time.
        limit: Optional; The maximum number of albums to return.  Default: 20.
          Minimum: 1. Maximum: 50.
        offset: Optional; The index of the first category to return. Default:
          0.
        """
        url = f'https://api.spotify.com/v1/browse/categories'
        query_params = {'country': country, 'locale': locale, 'timestamp': timestamp, 'limit': limit, 'offset': offset}
        json_body = {}
        response, error = self._get(url, query_params, json_body)
        if error:
            return ErrorObject(response)
        return PagingObject(response.text, CategoryObject)

    def get_a_category(self, category_id: str, country: str = None, locale: str = None) -> Union[
        CategoryObject, ErrorObject]:
        """
        Get a single category used to tag items in Spotify (on, for example, the
    Spotify player’s “Browse” tab).

    Args:
        category_id: The Spotify category ID for the category.
        country: Optional; An ISO 3166-1 alpha-2 country code or the string
          'from_token'.
        locale: Optional; The desired language, consisting of a lowercase ISO
          639-1 language code and an uppercase ISO 3166-1 alpha-2 country
          code, joined by an underscore. For example: es_MX, meaning “Spanish
          (Mexico)”. Provide this parameter if you want the results returned
          in a particular language (where available). Note that, if locale is
          not supplied, or if the specified language is not available, all
          strings will be returned in the Spotify default language (American
          English). The locale parameter, combined with the country parameter,
          may give odd results if not carefully matched.
        """
        url = f'https://api.spotify.com/v1/browse/categories/{category_id}'
        query_params = {'country': country, 'locale': locale}
        json_body = {}
        response, error = self._get(url, query_params, json_body)
        if error:
            return ErrorObject(response)
        return CategoryObject(response.text)
