# """Not currently used."""
# from webbrowser import open_new
# from flask import Flask, request
# import requests
# 
# app = Flask(__name__)
# 
# token_received = None
# 
# 
# @app.route('/get_token/')
# def token_request():
#     return '''
# <h1>Received key. Sending it back to Python...</h1>
# <script type="text/javascript">
# 
# var hash = false; 
# checkHash();
# 
# function checkHash(){ 
#     if(window.location.hash != hash) { 
#         hash = window.location.hash; 
#         processHash(hash.replace("#", "?")); 
#     }
# }
# 
# function processHash(hash){
#     window.location.replace('http://localhost:8080/post_token/'+hash);
# }
#                 
# </script> 
# '''
# 
# 
# @app.route('/post_token/')
# def token_response():
#     global token_received
#     token_received = request.args['access_token']
# 
#     func = request.environ.get('werkzeug.server.shutdown')
#     func()
#     return "<h1>Token received by Python. You can close this.</h1>"
# 
# 
# def construct_authorize_url(**params):
#     base = 'https://accounts.spotify.com/authorize/?'
#     return base + '&'.join([f'{key}={value}' for key, value in params.items()])
# 
# 
# def request_token(url):
#     print('opening URL')
#     open_new(url)
# 
# 
# def get_token(port: int = 8080) -> str:
#     app.run(port=port)
#     return token_received
# 
# 
# if __name__ == '__main__':
#     authorize_url = construct_authorize_url(
#         client_id='5b35c8171b7f41bfb1f134c909b5e3ec',
#         redirect_uri='http://localhost:8080/get_token/',
#         scope='user-read-recently-played%20'
#               'user-top-read%20'
#               'user-read-playback-position%20'
#               'user-modify-playback-state%20'
#               'user-read-playback-state%20'
#               'user-read-currently-playing',
#         response_type='token',
#         state='123')
#     request_token(authorize_url)
#     token = get_token()
#     print(f'**run_sever() received {token}')
# 
# 
# def do(api_url):
#     return requests.get(api_url, headers={
#         'Accept': 'application/json',
#         'Content-Type': 'application/json',
#         'Authorization': f'Bearer {token}'
#     })
