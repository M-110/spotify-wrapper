from typing import Callable, List
from functools import wraps
import inspect

def requires(scopes: List[str]) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def inner(self, *args, **kwargs):
            if any(scope not in self.scopes for scope in scopes):
                raise PermissionError(f'{func.__name__} requires the {scopes!r} scope. You must have this scope authorized to make this API call.')
            else:
                return func(self, *args, **kwargs)
        return inner
    return decorator            
    