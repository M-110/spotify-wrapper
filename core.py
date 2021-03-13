from server_pkce_flow import get_new_credentials
import requests


class SpotifyAPI:
    HTTP_METHODS = {'POST': requests.post,
                    'GET': requests.get,
                    'PUT': requests.put}

    def __init__(self):
        self._credentials: dict = get_new_credentials()
        self._access_token: str = self._credentials['access_token']
        self.headers = {'Accept': 'application/json',
                        'Content-Type': 'application/json',
                        'Authorization': f'Bearer {self._access_token}'}

    def _get(self, endpoint):
        return requests.get(endpoint, headers=self.headers)

    def get_current_users_profile(self):
        return self._get('https://api.spotify.com/v1/me')
