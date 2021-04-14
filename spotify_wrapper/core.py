import requests
from typing import Optional
from .authorization_flow.server_pkce_flow import get_new_credentials
from .object_library import AlbumObject
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
        query_params ={key: value for key, value in query_params.items() if value is not None}
        print(f'{url=}')
        print(f'{query_params=}')
        print(f'{json_body=}')
        result = requests.get(url, params=query_params, headers=self.headers)
        print(result.text)
        return result

    def _put(self, endpoint):
        return requests.put(endpoint, headers=self.headers)

    def _post(self, endpoint):
        return requests.post(endpoint, headers=self.headers)

    @requires(['user-read-email', 'user-read-private'])
    def get_current_users_profile(self):
        return self._get('https://api.spotify.com/v1/me')

    @requires(['user-modify-playback-state'])
    def play_next_song(self):
        return self._post('https://api.spotify.com/v1/me/player/next')

    def get_an_album(self, id_: str, market: str = None) -> Optional[AlbumObject]:
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
        response = self._get(url, query_params, json_body)
        return AlbumObject(response.text)

    def get_a_category(self, category_id, country):
        return requests.get(f'https://api.spotify.com/v1/browse/categories/{category_id}',
                            params={'country': country},
                            headers=self.headers)

# s = SpotifyAPI()

# r = s.get_a_category('dinner', 'SE')
# print(r.request.url)
