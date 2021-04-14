from typing import Callable, List
from functools import wraps


# TODO: This seems really specific to one class. Maybe it should be closer to it?
def requires(scopes: List[str]) -> Callable:
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
                raise PermissionError(f'{func.__name__} requires the {scopes!r} '
                                      'scope. You must have this scope authorized '
                                      'to make this API call.')
            else:
                return func(self, *args, **kwargs)

        return inner

    return decorator
