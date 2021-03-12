from requests import session, Response, Session
import requests
from webbrowser import open_new
from urllib.request import urlopen



url = 'https://accounts.spotify.com/authorize'
client_id = '5b35c8171b7f41bfb1f134c909b5e3ec'
response_type = 'token'
uri = 'https://www.spotify.com/'
scopes = ' '.join(['user-read-recently-played',
          'user-top-read',
          'user-read-playback-position',
          'user-read-playback-state',
          'user-read-currently-playing'])

payload = {'client_id':'5b35c8171b7f41bfb1f134c909b5e3ec',
           'redirect_uri': 'http://localhost:8080/get_token/',
           'scope': 'user-read-recently-played%20'
                    'user-top-read%20'
                    'user-read-playback-position%20'
                    'user-modify-playback-state%20'
                    'user-read-playback-state%20'
                    'user-read-currently-playing',
           'response_type': 'token',
            'state': '123'
            }

params = [f'{key}={value}' for key, value in payload.items()]
params = '&'.join(params)


print(f'{url}?{params}')
open_new(f'{url}?{params}')


a = requests.get(url, params=payload)

