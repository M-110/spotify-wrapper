from webbrowser import open_new
from flask import Flask, request
import requests
from string import ascii_letters
import random
from hashlib import sha256
import base64
import json
from urllib.parse import urlencode
from typing import Tuple, Optional

app = Flask(__name__)

authorization_code: Optional[str] = None
credentials: Optional[dict] = None
state = str(random.randint(1, 999))
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
                       'user-read-private',])


def _missing_credentials() -> bool:
    """Returns True if 'credentials.json' could not be found or
    if it doesn't contain a refresh token."""
    try:
        with open('credentials.json', 'r') as credentials_json:
            global credentials
            credentials = json.load(credentials_json)
            print('\n\nloaded credentials from json:' + str(credentials))
            return False
    except FileNotFoundError:
        print('Could not find credentials.json.')
        return True


def _generate_code_challenge() -> Tuple[bytes, str]:
    """Generates a random code and encodes is with sha256 and base64.
    
    Returns:
        code_verifier: randomly generated string which will be used for getting
                       the token from Spotify.
        code_challenge: encoded form of code_verifier which will be used for
                        getting the code from Spotify.
    """
    code_verifier = ''.join([random.choice(ascii_letters) for _ in range(44)]).encode('utf-8')
    sha = sha256(code_verifier).digest()
    code_challenge = base64.urlsafe_b64encode(sha).decode('utf-8')[:-1]
    return code_verifier, code_challenge


def _construct_authorize_url(code_challenge: str) -> str:
    """Returns a string of the authorization url."""
    base = 'https://accounts.spotify.com/authorize/?'
    return base + urlencode(dict(
        client_id='5b35c8171b7f41bfb1f134c909b5e3ec',
        response_type='code',
        redirect_uri='http://localhost:8080/get_token/',
        code_challenge_method='S256',
        code_challenge=code_challenge,
        state=state,
        scope=SCOPE))


def _get_authorization(code_challenge: str):
    """Get the authorization code and store as the global variable 'authorization_code'.
    
    This will open a browser for the client to authorize the app, and run a
    local Flask server to receive the code.
    """
    authorize_url: str = _construct_authorize_url(code_challenge)

    # Open the authorization page in a browser window.
    open_new(authorize_url)

    # Run a temporary server to receive the code from Spotify which will
    # be sent to localhost:8080/get_token/ through the redirect URI
    # after the client approves authorization.
    app.run(port=8080)

    # Once the server receives a response, the _token_request function will
    # be called which will store the authorization_code as a global variable
    # and then the server will shut itself down and this code will continue.
    return


@app.route('/get_token/')
def _token_request():
    global authorization_code
    authorization_code = request.args.get('code', None)

    if state != request.args.get('state'):
        print('State did not match... Quitting.')
        quit()

    request.environ.get('werkzeug.server.shutdown')()

    if authorization_code is None:
        return "Something went wrong. Where is the code?"
    else:
        return f"<h1>WE GOT IT, WE GOT THE CODE!! IT IS:</h1> <br> {authorization_code}"


def _get_token_json(code_verifier: bytes):
    base_url = 'https://accounts.spotify.com/api/token'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    params = dict(
        client_id='5b35c8171b7f41bfb1f134c909b5e3ec',
        grant_type='authorization_code',
        code=authorization_code,
        redirect_uri='http://localhost:8080/get_token/',
        code_verifier=code_verifier
    )
    global credentials
    credentials = requests.post(base_url, data=params, headers=headers).json()


def _refresh_credentials():
    global credentials
    base_url = 'https://accounts.spotify.com/api/token'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    params = dict(
        client_id='5b35c8171b7f41bfb1f134c909b5e3ec',
        grant_type='refresh_token',
        refresh_token=credentials['refresh_token']
    )
    credentials = requests.post(base_url, data=params, headers=headers).json()
    _save_credentials()


def _save_credentials():
    with open('credentials.json', 'w') as credentials_json:
        global credentials
        credentials_json.write(json.dumps(credentials))
        print("Saved credentials" + str(credentials))


def _confirm_token_in_credentials() -> bool:
    try:
        return bool(credentials['access_token'])
    except KeyError:
        return False


def get_new_credentials() -> dict:
    if _missing_credentials():
        code_verifier, code_challenge = _generate_code_challenge()
        _get_authorization(code_challenge)
        _get_token_json(code_verifier)

    _refresh_credentials()

    if _confirm_token_in_credentials():
        return credentials
    else:
        raise ValueError("Something went wrong with the credentials. Could not find authorization token.")
