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


class PrivateUserObject:
    def __init__(self, json_string: str):
        self._json_string = json_string
        self._set_attributes()

    def _set_attributes(self, json_string: str):
        obj_dict = json.loads(json_string)
        self._country: str = str(obj_dict['country'])
        self._display_name: str = obj_dict['display_name']
        self._email = obj_dict['email']
        self._explicit_content = obj_dict['explicit_content']
        self._external_urls = obj_dict['external_urls']
        self._followers = obj_dict['followers']
        self._href = obj_dict['href']
        self._id = obj_dict['id']
        self._images = obj_dict['images']
        self._product = obj_dict['product']
        self._type = obj_dict['type']
        self._uri = obj_dict['uri']

    @property
    def country(self):
        return self.json_string['country']
    
class PagingObject(Iterable[T], SpotifyObject):
    
    def _set_attributes(self, json_string: str):
        pass
        


class AlbumObject(SpotifyObject):
    """Obj."""

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
        return self._ablum_type
        
    @property
    def artists(self) -> List[ArtistObject]:
        """
        The artists of the album. Each artist object includes a link in
        href to more detailed information about the artist.
        """
        return self._artists
        
        


class AlbumRestrictionObject(SpotifyObject):
    """Obj."""

    def _set_attributes(self, json_dict: dict):
        ...


class ArtistObject(SpotifyObject):
    """Obj."""

    def _set_attributes(self, json_dict: dict):
        ...


class AudioFeaturesObject(SpotifyObject):
    """Obj."""

    def _set_attributes(self, json_dict: dict):
        ...


class CategoryObject(SpotifyObject):
    """Obj."""

    def _set_attributes(self, json_dict: dict):
        ...


class ContextObject(SpotifyObject):
    """Obj."""

    def _set_attributes(self, json_dict: dict):
        ...


class CopyrightObject(SpotifyObject):
    """Obj."""

    def _set_attributes(self, json_dict: dict):
        ...


class CurrentlyPlayingContextObject(SpotifyObject):
    """Obj."""

    def _set_attributes(self, json_dict: dict):
        ...


class CurrentlyPlayingObject(SpotifyObject):
    """Obj."""

    def _set_attributes(self, json_dict: dict):
        ...


class CursorObject(SpotifyObject):
    """Obj."""

    def _set_attributes(self, json_dict: dict):
        ...


class CursorPagingObject(SpotifyObject):
    """Obj."""

    def _set_attributes(self, json_dict: dict):
        ...


class DeviceObject(SpotifyObject):
    """Obj."""

    def _set_attributes(self, json_dict: dict):
        ...


class DevicesObject(SpotifyObject):
    """Obj."""

    def _set_attributes(self, json_dict: dict):
        ...


class DisallowsObject(SpotifyObject):
    """Obj."""

    def _set_attributes(self, json_dict: dict):
        ...


class EpisodeObject(SpotifyObject):
    """Obj."""

    def _set_attributes(self, json_dict: dict):
        ...


class ErrorObject(SpotifyObject):
    """Obj."""

    def _set_attributes(self, json_dict: dict):
        ...


class ExplicitContentSettingsObject(SpotifyObject):
    """Obj."""

    def _set_attributes(self, json_dict: dict):
        ...


class ExternalIdObject(SpotifyObject):
    """Obj."""

    def _set_attributes(self, json_dict: dict):
        ...


class ExternalUrlObject(SpotifyObject):
    """Obj."""

    def _set_attributes(self, json_dict: dict):
        ...


class FollowersObject(SpotifyObject):
    """Obj."""

    def _set_attributes(self, json_dict: dict):
        ...


class ImageObject(SpotifyObject):
    """Obj."""

    def _set_attributes(self, json_dict: dict):
        ...


class LinkedTrackObject(SpotifyObject):
    """Obj."""

    def _set_attributes(self, json_dict: dict):
        ...


class PagingObject(SpotifyObject):
    """Obj."""

    def _set_attributes(self, json_dict: dict):
        ...


class PlayHistoryObject(SpotifyObject):
    """Obj."""

    def _set_attributes(self, json_dict: dict):
        ...


class PlayerErrorObject(SpotifyObject):
    """Obj."""

    def _set_attributes(self, json_dict: dict):
        ...


class PlaylistObject(SpotifyObject):
    """Obj."""

    def _set_attributes(self, json_dict: dict):
        ...


class PlaylistTrackObject(SpotifyObject):
    """Obj."""

    def _set_attributes(self, json_dict: dict):
        ...


class PlaylistTracksRefObject(SpotifyObject):
    """Obj."""

    def _set_attributes(self, json_dict: dict):
        ...


class PrivateUserObject(SpotifyObject):
    """Obj."""

    def _set_attributes(self, json_dict: dict):
        ...


class PublicUserObject(SpotifyObject):
    """Obj."""

    def _set_attributes(self, json_dict: dict):
        ...


class RecommendationSeedObject(SpotifyObject):
    """Obj."""

    def _set_attributes(self, json_dict: dict):
        ...


class RecommendationsObject(SpotifyObject):
    """Obj."""

    def _set_attributes(self, json_dict: dict):
        ...


class ResumePointObject(SpotifyObject):
    """Obj."""

    def _set_attributes(self, json_dict: dict):
        ...


class SavedAlbumObject(SpotifyObject):
    """Obj."""

    def _set_attributes(self, json_dict: dict):
        ...


class SavedEpisodeObject(SpotifyObject):
    """Obj."""

    def _set_attributes(self, json_dict: dict):
        ...


class SavedShowObject(SpotifyObject):
    """Obj."""

    def _set_attributes(self, json_dict: dict):
        ...


class SavedTrackObject(SpotifyObject):
    """Obj."""

    def _set_attributes(self, json_dict: dict):
        ...


class ShowObject(SpotifyObject):
    """Obj."""

    def _set_attributes(self, json_dict: dict):
        ...


class SimplifiedAlbumObject(SpotifyObject):
    """Obj."""

    def _set_attributes(self, json_dict: dict):
        ...


class SimplifiedArtistObject(SpotifyObject):
    """Obj."""

    def _set_attributes(self, json_dict: dict):
        ...


class SimplifiedEpisodeObject(SpotifyObject):
    """Obj."""

    def _set_attributes(self, json_dict: dict):
        ...


class SimplifiedPlaylistObject(SpotifyObject):
    """Obj."""

    def _set_attributes(self, json_dict: dict):
        ...


class SimplifiedShowObject(SpotifyObject):
    """Obj."""

    def _set_attributes(self, json_dict: dict):
        ...


class SimplifiedTrackObject(SpotifyObject):
    """Obj."""

    def _set_attributes(self, json_dict: dict):
        ...


class TrackObject(SpotifyObject):
    """Obj."""

    def _set_attributes(self, json_dict: dict):
        ...


class TrackRestrictionObject(SpotifyObject):
    """Obj."""

    def _set_attributes(self, json_dict: dict):
        ...


class TuneableTrackObject(SpotifyObject):
    """Obj."""

    def _set_attributes(self, json_dict: dict):
        ...
