from server_pkce_flow import create_token
import requests


def do(api_url, token):
    return requests.post(api_url, headers={
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    })


if __name__ == "__main__":
    token = create_token()
    do('https://api.spotify.com/v1/me/player/next/', token)
    