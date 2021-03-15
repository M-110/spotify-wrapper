from __future__ import annotations

import json
from collections.abc import Iterable
from typing import List, Optional, TypeVar, Generic

T = TypeVar('T')


class SpotifyObject:
    """Baby cat."""

    def __init__(self, json_object: Optional[str, dict]):
        if isinstance(json_object, dict):
            self._json_string = json.dumps(json_object)
            self._json_dict = json_object
        elif isinstance(json_object, str):
            self._json_string = json_object
            self._json_dict = json.loads(json_object)

        self._set_attributes(self._json_dict)

    def _set_attributes(self, json_dict: dict):
        ...


class AlbumObject(SpotifyObject):
    """Album Object Doc String"""

    def _set_attributes(self, json_dict: dict):
        self._album_type: str = json_dict['album_type']
        self._artists: List[ArtistObject] = json_dict['artists']
        self._available_markets: List[str] = json_dict['available_markets']
        self._copyrights: List[CopyrightObject] = json_dict['copyrights']
        self._external_ids: ExternalIdObject = json_dict['external_ids']
        self._external_urls: ExternalUrlObject = json_dict['external_urls']
        self._genres: List[str] = json_dict['genres']
        self._href: str = json_dict['href']
        self._id: str = json_dict['id']
        self._images: List[ImageObject] = json_dict['images']
        self._label: str = json_dict['label']
        self._name: str = json_dict['name']
        self._popularity: int = json_dict['popularity']
        self._release_date: str = json_dict['release_date']
        self._release_date_precision: str = json_dict['release_date_precision']
        self._restrictions: Optional[AlbumRestrictionObject] = json_dict.get('restrictions')
        self._tracks: PagingObject[SimplifiedTrackObject] = json_dict['tracks']
        self._type: str = json_dict['type']
        self._uri: str = json_dict['uri']

    @property
    def album_type(self) -> str:
        """
        The type of the album: album, single, or compilation.
        """
        return self._json_dict['album_type']
    
    
class CopyrightObject(SpotifyObject):
    pass


class ArtistObject(SpotifyObject):
    pass


class ExternalIdObject(SpotifyObject):
    pass


class ExternalUrlObject(SpotifyObject):
    pass


class ImageObject(SpotifyObject):
    pass


class AlbumRestrictionObject(SpotifyObject):
    pass


class SimplifiedTrackObject(SpotifyObject):
    pass


class PagingObject(Iterable[T], SpotifyObject):
    pass

