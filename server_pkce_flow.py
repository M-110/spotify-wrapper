from webbrowser import open_new
from flask import Flask, request
from threading import Thread
import time
import requests
from string import ascii_letters
import random
from hashlib import sha256
import base64

app = Flask(__name__)

authorization_code = None
state = str(random.randint(1,999))


def generate_code_challenge() -> (str, str):
    """Generates a random code and encodes is with sha256 and base64."""
    code_verifier = ''.join([random.choice(ascii_letters) for _ in range(44)]).encode('utf-8')
    sha = sha256(code_verifier).digest()
    code_challenge = base64.urlsafe_b64encode(sha).decode('utf-8')[:-1]
    return code_verifier, code_challenge

@app.route('/get_token/')
def token_request():
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

def construct_authorize_url(**params):
    base = 'https://accounts.spotify.com/authorize/?'
    return base + '&'.join([f'{key}={value}' for key, value in params.items()])

def construct_token_url(code, code_verifier):
    base_url = 'https://accounts.spotify.com/api/token'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    params = dict(
        client_id = '5b35c8171b7f41bfb1f134c909b5e3ec',
        grant_type = 'authorization_code',
        code = code,
        redirect_uri = 'http://localhost:8080/get_token/',
        code_verifier = code_verifier
        )
    json_response = requests.post(base_url, data=params, headers=headers).json()
    access_token = json_response['access_token']
    scope = json_response['scope']
    expires_in = json_response['expires_in']
    refresh_token = json_response['refresh_token']
    print(f'{access_token=}')
    print(f'{scope=}')
    print(f'{expires_in=}')
    print(f'{refresh_token=}')
    

def request_token(url):
    print('opening URL')
    open_new(url)
    
        

def get_authorization_code(port: int = 8080) -> str:
    app.run(port=port)
    return authorization_code
        
    

if __name__ == '__main__':
    code_verifier, code_challenge = generate_code_challenge()
    
    authorize_url = construct_authorize_url(
        client_id = '5b35c8171b7f41bfb1f134c909b5e3ec',
        response_type = 'code',
        redirect_uri = 'http://localhost:8080/get_token/',
        code_challenge_method = 'S256',
        code_challenge = code_challenge,
        state = state,
        scope = 'user-follow-modify'
        )
    
    request_token(authorize_url)
    auth_code = get_authorization_code()
    print(f'**run_sever() received {auth_code}')
    
    construct_token_url(authorization_code, code_verifier)
    
    
    

token = None
def do(api_url):
    return requests.get(api_url, headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {token}'
    })

def refresh_token():
    base_url = 'https://accounts.spotify.com/api/token'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    params = dict(
        client_id = '5b35c8171b7f41bfb1f134c909b5e3ec',
        grant_type = 'refresh_token',
        refresh_token = 'AQDox7X0bHZ3uedFLX-ThhSzkhaaymkXqSoE71zNW8kD5VLRDYE3W3UAy5cJFRTfLAiAsZExwURv_hNz5htdPNKH2RNesCkJuEDoR7U-S3gyFgRnF9eODzXn0UlHx0ZonOQ'
        )
    json_response = requests.post(base_url, data=params, headers=headers).json()
    print(json_response)
    


