"""Testing script"""
import requests

from spotifywrapper.authentication import authorization_code_flow_pkce as pkce


def pkce_flow():
    """Test getting a profile through PKCE"""
    token = pkce.PKCE().get_credentials()['access_token']

    headers = {'Accept': 'application/json',
               'Content-Type': 'application/json',
               'Authorization': f'Bearer {token}'}

    profile = requests.get('https://api.spotify.com/v1/me', headers=headers
                           ).json()
    return profile


if __name__ == '__main__':
    print(f'Received profile through pkce: {pkce_flow()}')
