"""Authorization Code Flow with Proof Key for Code Exchange (PKCE)"""
import base64
import secrets
from hashlib import sha256
import json
from json import JSONDecodeError
from typing import Tuple, Optional, TypedDict
from urllib.parse import urlencode
import webbrowser

import requests
from requests.exceptions import RequestException

from .custom_http_server import (
    retrieve_authorization_code_using_local_http_server)

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


class Credentials(TypedDict):
    """TypedDict representing the json response data returned from the
    Spotify authorization process."""
    access_token: str
    token_type: str
    scope: str
    expires_in: int
    refresh_token: str


class PKCE:
    """PKCE flow authentication."""

    def __init__(self) -> None:
        self._authorization_code: Optional[str] = None
        self._credentials: Optional[Credentials] = None
        self._state = secrets.token_urlsafe(10)
        self._code_verifier_length = 64
        self._server_address = ('localhost', 8080)
        self._redirect_uri = 'http://localhost:8080/get_token/'
        self._client_id = '5b35c8171b7f41bfb1f134c909b5e3ec'
        self._credentials_filename = 'credentials.json'

    @property
    def server_address(self) -> Tuple[str, int]:
        """Returns server address."""
        return self._server_address

    @property
    def state(self) -> str:
        """Returns the state (for CSRF purposes)"""
        return self._state

    def get_credentials(self) -> Credentials:
        """Get credentials containing the API access token.

        It will first try to open the credentials.json file and refresh the
        credentials using a refresh token saved in the file. If this fails,
        it will then will ask the user to authorize the app in a browser,
        and Spotify will return an access token.

        The new or refreshed token will then be saved in the
        credentials.json file.

        Returns:
            Credentials: A credentials dictionary from Spotify that contains an
                access token required for API calls.
        """
        try:
            self._refresh_old_credentials()
        except (JSONDecodeError, FileNotFoundError, KeyError,
                RequestException):
            self._create_new_credentials()
        self._save_credentials_to_local_json_file()
        return self._credentials

    def _refresh_old_credentials(self) -> None:
        """Get the previously saved credentials from the credentials.json
        file and use the refresh token to get a new updated access token.

        Raises:
            FileNotFoundError: If the credentials.json could not be located
                in the current directory.
            JSONDecodeError: If the json file has invalid json data or the
                request returns invalid json data.
            KeyError: If the credentials json did not have a refresh token.
            RequestException: If the post request fails.
        """
        with open(self._credentials_filename, encoding='utf8') as json_file:
            self._credentials = json.load(json_file)
        self._get_access_token_using_refresh_token()

    def _get_access_token_using_refresh_token(self) -> None:
        """Send a request to spotifywrapper for new credentials using the current
        refresh token.

        Stores the new credentials as self._credentials.

        Raises:
            KeyError: If the credentials json did not have a refresh token.
            RequestException: If the request fails.
            JSONDecodeError: If the post request fails.
        """
        base_url = 'https://accounts.spotify.com/api/token'
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        params = dict(
            client_id=self._client_id,
            grant_type='refresh_token',
            refresh_token=self._credentials['refresh_token']
        )
        self._credentials = requests.post(base_url, data=params,
                                          headers=headers).json()

    def _create_new_credentials(self) -> None:
        """Generate a code challenge, have the user authorize the app
        using the authorization URI, and then exchange the authorization
        code for an access token.

        The new credentials will be stored as self._credentials.
        """
        verifier, challenge = self._generate_code_verifier_and_challenge()
        self._get_authorization_code(challenge)
        self._get_access_token_using_authorization_code(verifier)

    def _generate_code_verifier_and_challenge(self) -> Tuple[bytes, str]:
        """Generates a random code and encodes is with sha256 and base64.

        Returns:
            code_verifier: randomly generated string which will be used for
                getting the token from Spotify.
            code_challenge: encoded form of code_verifier which will be used
                forgetting the code from Spotify.
        """
        code_verifier = secrets.token_urlsafe(
            self._code_verifier_length).encode('utf8')
        code_hash = sha256(code_verifier).digest()
        code_challenge = base64.urlsafe_b64encode(code_hash).decode('utf-8')[
                         :-1]
        return code_verifier, code_challenge

    def _get_authorization_code(self, code_challenge: str) -> None:
        """Open an app authorization page for the user in their browser and
        receive the authorization code that Spotify returns through the
        redirect URI which will be handled by a local HTTP server.

        The authorization code will be stored as self._authorization_code.
        """
        authorize_url = self._construct_authorize_url(code_challenge)
        webbrowser.open_new(authorize_url)
        retrieve_authorization_code_using_local_http_server(self)

    def _construct_authorize_url(self, code_challenge: str) -> str:
        """Returns a string of the authorization url."""
        base = 'https://accounts.spotify.com/authorize/?'
        return base + urlencode(dict(
            client_id=self._client_id,
            response_type='code',
            redirect_uri=self._redirect_uri,
            code_challenge_method='S256',
            code_challenge=code_challenge,
            state=self._state,
            scope=SCOPE))

    def _get_access_token_using_authorization_code(self, code_verifier: bytes
                                                   ) -> None:
        """Use the authorization code to request an access token from
        Spotify.

        The new credentials will be stored as self._credentials.
        """
        base = 'https://accounts.spotify.com/api/token'
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        params = dict(
            client_id=self._client_id,
            grant_type='authorization_code',
            code=self._authorization_code,
            redirect_uri=self._redirect_uri,
            code_verifier=code_verifier
        )
        self._credentials = requests.post(base, data=params,
                                          headers=headers).json()

    def _save_credentials_to_local_json_file(self) -> None:
        """Save the current credentials as a .json file in the local
        directory."""
        with open(self._credentials_filename, 'w') as credentials_json:
            credentials_json.write(json.dumps(self._credentials))
