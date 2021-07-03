# from __future__ import annotations
# 
# import json
# from collections.abc import Iterable
# from typing import List, Optional, TypeVar, Generic
# 
# T = TypeVar('T')
# 
# 
# class SpotifyObject:
#     """Baby cat."""
# 
#     def __init__(self, json_object: Optional[str, dict]):
#         if isinstance(json_object, dict):
#             self._json_string = json.dumps(json_object)
#             self._json_dict = json_object
#         elif isinstance(json_object, str):
#             self._json_string = json_object
#             self._json_dict = json.loads(json_object)
# 
#         self._set_attributes(self._json_dict)
# 
#     def _set_attributes(self, json_dict: dict):
#         ...
# 
# 
# class AlbumObject(SpotifyObject):
#     """Album Object Doc String"""
# 
#     def _set_attributes(self, json_dict: dict):
#         self._album_type: str = json_dict['album_type']
#         self._artists: List[ArtistObject] = json_dict['artists']
#         self._available_markets: List[str] = json_dict['available_markets']
#         self._copyrights: List[CopyrightObject] = json_dict['copyrights']
#         self._external_ids: ExternalIdObject = json_dict['external_ids']
#         self._external_urls: ExternalUrlObject = json_dict['external_urls']
#         self._genres: List[str] = json_dict['genres']
#         self._href: str = json_dict['href']
#         self._id: str = json_dict['id']
#         self._images: List[ImageObject] = json_dict['images']
#         self._label: str = json_dict['label']
#         self._name: str = json_dict['name']
#         self._popularity: int = json_dict['popularity']
#         self._release_date: str = json_dict['release_date']
#         self._release_date_precision: str = json_dict['release_date_precision']
#         self._restrictions: Optional[AlbumRestrictionObject] = json_dict.get('restrictions')
#         self._tracks: PagingObject[SimplifiedTrackObject] = json_dict['tracks']
#         self._type: str = json_dict['type']
#         self._uri: str = json_dict['uri']
# 
#     @property
#     def album_type(self) -> str:
#         """
#         The type of the album: album, single, or compilation.
#         """
#         return self._json_dict['album_type']
#     
#     
# class CopyrightObject(SpotifyObject):
#     pass
# 
# 
# class ArtistObject(SpotifyObject):
#     pass
# 
# 
# class ExternalIdObject(SpotifyObject):
#     pass
# 
# 
# class ExternalUrlObject(SpotifyObject):
#     pass
# 
# 
# class ImageObject(SpotifyObject):
#     pass
# 
# 
# class AlbumRestrictionObject(SpotifyObject):
#     pass
# 
# 
# class SimplifiedTrackObject(SpotifyObject):
#     pass
# 
# 
# class PagingObject(Iterable[T], SpotifyObject):
#     pass
# 
# class AlbumObject(SpotifyObject):
#     """Album Object Doc String."""
# 
#     @property
#     def album_type(self) -> str:
#         """
#         The type of the album: album, single, or compilation.
#         """
#         return self._json_dict['album_type']
# 
#     @property
#     def artists(self) -> List[str]:
#         """
#         The artists of the album. Each artist object includes a link in href to more detailed information about the artist.
#         """
#         return self._json_dict['artists']
# 
#     @property
#     def available_markets(self) -> List[str]:
#         """
#         The markets in which the album is available: ISO 3166-1 alpha-2 country codes. Note that an album is considered available in a market when at least 1 of its tracks is available in that market.
#         """
#         return self._json_dict['available_markets']
# 
#     @property
#     def copyrights(self) -> List[ArtistObject]:
#         """
#         The copyright statements of the album.
#         """
#         return self._json_dict['copyrights']
# 
#     @property
#     def external_ids(self) -> ExternalIdObject:
#         """
#         Known external IDs for the album.
#         """
#         return self._json_dict['external_ids']
# 
#     @property
#     def external_urls(self) -> ExternalUrlObject:
#         """
#         Known external URLs for this album.
#         """
#         return self._json_dict['external_urls']
# 
#     @property
#     def genres(self) -> List[str]:
#         """
#         A list of the genres used to classify the album. For example: “Prog Rock” , “Post-Grunge”. (If not yet classified, the array is empty.)
#         """
#         return self._json_dict['genres']
# 
#     @property
#     def href(self) -> str:
#         """
#         A link to the Web API endpoint providing full details of the album.
#         """
#         return self._json_dict['href']
# 
#     @property
#     def id(self) -> str:
#         """
#         The Spotify ID for the album.
#         """
#         return self._json_dict['id']
# 
#     @property
#     def images(self) -> List[ImageObject]:
#         """
#         The cover art for the album in various sizes, widest first.
#         """
#         return self._json_dict['images']
# 
#     @property
#     def label(self) -> str:
#         """
#         The label for the album.
#         """
#         return self._json_dict['label']
# 
#     @property
#     def name(self) -> str:
#         """
#         The name of the album. In case of an album takedown, the value may be an empty string.
#         """
#         return self._json_dict['name']
# 
#     @property
#     def popularity(self) -> int:
#         """
#         The popularity of the album. The value will be between 0 and 100, with 100 being the most popular. The popularity is calculated from the popularity of the album’s individual tracks.
#         """
#         return self._json_dict['popularity']
# 
#     @property
#     def release_date(self) -> str:
#         """
#         The date the album was first released, for example “1981-12-15”. Depending on the precision, it might be shown as “1981” or “1981-12”.
#         """
#         return self._json_dict['release_date']
# 
#     @property
#     def release_data_precision(self) -> str:
#         """
#         The precision with which release_date value is known: “year” , “month” , or “day”.
#         """
#         return self._json_dict['release_data_precision']
# 
#     @property
#     def restrictions(self) -> AlbumRestrictionObject:
#         """
#         Included in the response when a content restriction is applied. See Restriction Object for more details.
#         """
#         return self._json_dict['restrictions']
# 
#     @property
#     def tracks(self) -> PagingObject[SimplifiedTrackObject]:
#         """
#         The tracks of the album.
#         """
#         return self._json_dict['tracks']
# 
#     @property
#     def type(self) -> str:
#         """
#         The object type: “album”.
#         """
#         return self._json_dict['type']
# 
#     @property
#     def uri(self) -> str:
#         """
#         The Spotify URI for the album.
#         """
#         return self._json_dict['uri']