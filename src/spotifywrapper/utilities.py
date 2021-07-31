import json
import pickle
from typing import Callable, List, Tuple
from dataclasses import dataclass
from functools import wraps


def requires(*scopes: str) -> Callable:
    """
    Adds a validator to SpotifyAPI methods which will check to make sure the
    method's scope is within the API token's scope.

    Args:
        scopes: A list of scopes from the Spotify API.
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def inner(self, *args, **kwargs):
            if any(scope not in self.scopes for scope in scopes):
                raise PermissionError(
                    f'{func.__name__} requires the {scopes!r} '
                    'scope. You must have this scope authorized '
                    'to make this API call.')
            else:
                return func(self, *args, **kwargs)

        return inner

    return decorator


# TODO: It caches result across all instances.
def cached_static_property(method):
    cached_result = None

    @wraps(method)
    def inner(self):
        nonlocal cached_result
        if cached_result is None:
            cached_result = method(self)
        return cached_result

    return property(inner)

def cache_get_locally(method):
    """Cache the results in a local method."""

    @wraps(method)
    def inner(url, query_params, json_body):
        response, error = method(url, query_params, json_body)
        query_params = json.dumps(query_params, sort_keys=True)
        json_body = json.dumps(json_body, sort_keys=True)
        print(url)
        print(type(query_params))
        print(type(json_body))
        data = {(url, query_params, json_body): (response, error)}
        with open('cache.txt', 'wb') as file:
            pickle.dump(data, file)
        return response, error
    return inner



@dataclass
class CustomResponse:
    text: str
