"""Playground for testing the API"""
from hashlib import md5
import json
import os
import pathlib
import pickle

from spotifywrapper.api import SpotifyAPI


# TODO Add mock data container which will make a response object (needs
#  .json method)
class MockResponse:
    def __init__(self, text):
        self.text = text

def hash_args(url, query_params, json_body):
    """Hash the tuple of args"""
    query_params = json.dumps(query_params, sort_keys=True)
    json_body = json.dumps(json_body, sort_keys=True)
    request = url + query_params + json_body
    return md5(request.encode('utf8')).hexdigest()


def cache_get_locally(method):
    """Cache the results in a local method."""

    def inner(url, query_params, json_body):
        request_hash = hash_args(url, query_params, json_body)

        filename = os.path.join('mock_get_data', f'{request_hash}.json')

        if os.path.isfile(filename):
            with open(filename, encoding='utf8') as file:
                response = MockResponse(file.read())
                error = None
                print(f'Opened {filename}')
        else:
            response, error = method(url, query_params, json_body)
            print(response.text)
            with open(filename, 'w', encoding='utf8') as file:
                json.dump(response.json(), file)
                print(f'Saved as {filename}')

        return response, error

    return inner


album_power_in_numbers = '2w9KjhjN2oMGhEvE15HK5T'
album_monty_python = '2C9kceX8onhaGScmaT9xGC'


def run_gets(spotify):
    """Run through the gets to generate the mock data."""
    a = spotify.get_multiple_albums([album_monty_python,
                                    album_power_in_numbers])
    print(a)


# profile2 = sp.get_an_album('4QIZtPbEAQTu1smtYyDHXz')

if __name__ == '__main__':
    sp = SpotifyAPI()
    sp._get = cache_get_locally(sp._get)
    run_gets(sp)
