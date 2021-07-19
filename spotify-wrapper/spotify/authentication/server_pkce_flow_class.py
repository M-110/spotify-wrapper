import base64
from hashlib import sha256
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import random
from string import ascii_letters
from typing import Tuple, Optional
from urllib.parse import urlencode, parse_qs, urlsplit
import webbrowser

import requests

SCOPE: str = ' '.join(['ugc-image-upload',
                       'user-read-recently-played',
                       'user-top-read',
                       'user-read-playback-position',
                       'user-read-playback-state',
                       'user-modify-playback-state',
                       'user-read-currently-playing',
                       'app-remote-control',
                       'streaming',
                       'playlist-modify-public',
                       'playlist-modify-private',
                       'playlist-read-private',
                       'playlist-read-collaborative',
                       'user-follow-modify',
                       'user-follow-read',
                       'user-library-modify',
                       'user-library-read',
                       'user-read-email',
                       'user-read-private', ])


class PKCE:
    def __init__(self):
        self.authorization_code: Optional[str] = None
        self.credentials: Optional[dict] = None
        self.state = str(random.randint(1, 999))

    def get_new_credentials(self) -> dict:
        if self.is_missing_credentials():
            code_verifier, code_challenge = self.generate_code_challenge()
            self.get_authorization(code_challenge)
            self.get_token_json(code_verifier)

        self.refresh_credentials()

        if self.is_token_in_credentials():
            return self.credentials
        else:
            raise ValueError(
                "Something went wrong with the credentials. Could not"
                " find authorization token.")

    def is_missing_credentials(self) -> bool:
        """Returns True if 'credentials.json' could not be found or
        if it doesn't contain a refresh token."""
        try:
            with open('credentials.json', 'r') as credentials_json:
                self.credentials = json.load(credentials_json)
                print('\n\nloaded credentials from json:' +
                      str(self.credentials))
                return False
        except FileNotFoundError:
            print('Could not find credentials.json.')
            return True

    @staticmethod
    def generate_code_challenge() -> Tuple[bytes, str]:
        """Generates a random code and encodes is with sha256 and base64.

        Returns:
            code_verifier: randomly generated string which will be used for getting
                           the token from Spotify.
            code_challenge: encoded form of code_verifier which will be used for
                            getting the code from Spotify.
        """
        code_verifier = ''.join([random.choice(ascii_letters)
                                 for _ in range(44)]).encode('utf-8')
        sha = sha256(code_verifier).digest()
        code_challenge = base64.urlsafe_b64encode(sha).decode('utf-8')[:-1]
        return code_verifier, code_challenge

    def get_authorization(self, code_challenge: str):
        """Get the authorization code and store as the global variable
        'authorization_code'.

        This will open a browser for the client to authorize the app, and run a
        local HTTP server to receive the code.

        This is meant to remove all responsibility from the user for
        handling the code. And instead allow them to just click the
        authorization button and the package will handle the rest.
        """
        authorize_url: str = self.construct_authorize_url(code_challenge)

        # Open the authorization page in a browser window.
        webbrowser.open_new(authorize_url)

        # Run a temporary server to receive the code from Spotify which will
        # be sent to localhost:8080/get_token/ through the redirect URI
        # after the client approves authorization.
        server = HTTPServer(("localhost", 8080), TempServer)
        try:
            server.serve_forever()
        except:
            server.server_close()

        # Once the server receives a response, the token_request function
        # will be called which will store the authorization_code as a global
        # variable and then the server will shut itself down and this code
        # will continue.
        return

    def construct_authorize_url(self, code_challenge: str) -> str:
        """Returns a string of the authorization url."""
        base = 'https://accounts.spotify.com/authorize/?'
        return base + urlencode(dict(
            client_id='5b35c8171b7f41bfb1f134c909b5e3ec',
            response_type='code',
            redirect_uri='http://localhost:8080/get_token/',
            code_challenge_method='S256',
            code_challenge=code_challenge,
            state=self.state,
            scope=SCOPE))

    def get_token_json(self, code_verifier: bytes):
        base_url = 'https://accounts.spotify.com/api/token'
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        params = dict(
            client_id='5b35c8171b7f41bfb1f134c909b5e3ec',
            grant_type='authorization_code',
            code=authorization_code,
            redirect_uri='http://localhost:8080/get_token/',
            code_verifier=code_verifier
        )
        self.credentials = requests.post(base_url, data=params,
                                         headers=headers).json()

    def refresh_credentials(self):
        base_url = 'https://accounts.spotify.com/api/token'
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        params = dict(
            client_id='5b35c8171b7f41bfb1f134c909b5e3ec',
            grant_type='refresh_token',
            refresh_token=self.credentials['refresh_token']
        )
        self.credentials = requests.post(base_url, data=params,
                                         headers=headers).json()
        self.save_credentials()

    def save_credentials(self):
        with open('credentials.json', 'w') as credentials_json:
            credentials_json.write(json.dumps(self.credentials))
            print("Saved credentials" + str(self.credentials))

    def is_token_in_credentials(self) -> bool:
        try:
            return bool(self.credentials['access_token'])
        except KeyError:
            return False


class TempServer(BaseHTTPRequestHandler):
    """A temporary local server that will receive the token from Spotify."""

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        query = parse_qs(urlsplit(self.path).query)

        global authorization_code
        self.authorization_code = query['code'][0]
        response_state = query['state'][0]
        if response_state != self.state:
            raise ValueError("State did not match.")
        self.wfile.write(
            bytes("<h1>Token received. You may close this window.</h1>",
                  "utf-8"))
        raise KeyboardInterrupt

    def log_message(self, *_):
        """Override log method to disable requests being logged in the
        console."""
