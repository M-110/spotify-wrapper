from server_pkce_flow import get_new_credentials
from utilities import requires
import requests


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

    def _get(self, endpoint):
        return requests.get(endpoint, headers=self.headers)

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

    def get_album(self):
        return self._get('https://api.spotify.com/v1/albums/4aawyAB9vmqN3uQ7FjRGTy')

    def get_a_category(self, category_id, country):
        return requests.get(f'https://api.spotify.com/v1/browse/categories/{category_id}',
                            params={'country': country},
                            headers=self.headers)


s = SpotifyAPI()

r = s.get_a_category('dinner', 'SE')
print(r.request.url)
