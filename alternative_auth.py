from string import ascii_letters
import random
from hashlib import sha256
import base64
import requests

code = ''.join([random.choice(ascii_letters) for _ in range(44)]).encode('utf-8')
print(f'{code=}')
sha = sha256(code).digest()
print(f'{sha=}')
b64 = base64.urlsafe_b64encode(sha)
print(f'{b64=}')

code_challenge = b64[:-1].decode('utf-8')

print(f'{code_challenge=}')

base_url = 'https://accounts.spotify.com/authorize?'
params = dict(
    client_id = '5b35c8171b7f41bfb1f134c909b5e3ec',
    response_type = 'code',
    redirect_uri = 'http://localhost:8080/get_token/',
    code_challenge_method = 'S256',
    code_challenge = code_challenge,
    state = '123',
    scope = 'user-follow-modify'
    )

combined_url = base_url + '&'.join([f'{key}={value}' for key, value in params.items()])

print(combined_url)