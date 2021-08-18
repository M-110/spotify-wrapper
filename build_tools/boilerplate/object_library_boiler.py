from __future__ import annotations

from collections.abc import Sequence
from datetime import datetime
import json
from typing import Dict, List, Optional, Type, TypeVar, Union, Generic

# from .utilities import cached_static_property

T = TypeVar('T')


def union_parser(classes: List[Type[T]], value: Dict[str, str]) -> Union[T]:
    ...


class SpotifyObject:
    """Baby cat."""

    def __init__(self, json_object: Optional[str, dict]):
        if isinstance(json_object, dict):
            self._json_string = json.dumps(json_object)
            self._json_dict = json_object
        elif isinstance(json_object, str):
            self._json_string = json_object
            self._json_dict = json.loads(json_object)

        # TODO: What is this?
        # self._set_attributes(self._json_dict)

    def __repr__(self):
        return f'{self.__class__.__name__}({self._json_dict})'

    def __str__(self):
        return str(self._json_dict)

    def _set_attributes(self, json_dict: dict):
        ...


class PagingObject(Sequence, Generic[T], SpotifyObject):
    """
    PagingObject doc string...
    """

    def __init__(self, json_object: Optional[str, dict], item_type: Type[T]):
        json_dict = json_object
        print(json_dict.keys())
        if len(json_dict.keys()) < 3:
            json_object = list(json_dict.values())[-1]
        super().__init__(json_object)
        self.item_type = item_type

    def __getitem__(self, i):
        return self.items[i]

    def __len__(self):
        return len(self.items)

    def __repr__(self):
        return f'<PagingObject items={self.items}>'

    @property
    def href(self) -> str:
        """
        A link to the Web API endpoint returning the full result of the
        request.
        """
        return str(self._json_dict['href'])

    @property
    def items(self) -> List[T]:
        """
        The requested data.
        """
        return [self.item_type(item) for item in self._json_dict['items']]

    @property
    def limit(self) -> int:
        """
        The maximum number of items in the response (as set in the query or by
        default).
        """
        return int(self._json_dict['limit'])

    @property
    def next(self) -> Optional[str]:
        """
        URL to the next page of items. None if this is the last page.
        """
        if value := self._json_dict['next']:
            return str(value)
        return None

    @property
    def offset(self) -> int:
        """
        The offset of the items returned (as set in the query or by default).
        """
        return int(self._json_dict['offset'])

    @property
    def previous(self) -> Optional[str]:
        """
        URL to the previous page of items. None if this is the first page.
        """
        if value := self._json_dict['previous']:
            return str(value)
        return None

    @property
    def total(self) -> int:
        """
        The total number of items available to return.
        """
        return int(self._json_dict['total'])


