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

        self._set_attributes(self._json_dict)

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
        json_dict = json.loads(json_object)
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


class AlbumObject(SpotifyObject):
    """
    Album Object Doc String.
    """

    def __repr__(self):
        return f'<AlbumObject name={self.name!r}, id={self.id!r},' \
               f'artists={self.artists}>'

    @property
    def album_type(self) -> str:
        """
        The type of the album: album, single, or compilation.
        """
        return str(self._json_dict['album_type'])

    @property
    def artists(self) -> List[SimplifiedArtistObject]:
        """
        The artists of the album. Each artist object includes a link in href
        to more detailed information about the artist.
        """
        return [SimplifiedArtistObject(item) for item in self._json_dict['artists']]

    @property
    def available_markets(self) -> List[str]:
        """
        The markets in which the album is available: ISO 3166-1 alpha-2
        country codes. Note that an album is considered available in a market
        when at least 1 of its tracks is available in that market.
        """
        return [str(item) for item in self._json_dict['available_markets']]

    @property
    def copyrights(self) -> List[CopyrightObject]:
        """
        The copyright statements of the album.
        """
        return [CopyrightObject(item) for item in self._json_dict['copyrights']]

    @property
    def external_ids(self) -> ExternalIdObject:
        """
        Known external IDs for the album.
        """
        return ExternalIdObject(self._json_dict['external_ids'])

    @property
    def external_urls(self) -> ExternalUrlObject:
        """
        Known external URLs for this album.
        """
        return ExternalUrlObject(self._json_dict['external_urls'])

    @property
    def genres(self) -> List[str]:
        """
        A list of the genres used to classify the album. For example: “Prog
        Rock” , “Post-Grunge”. (If not yet classified, the array is empty.)
        """
        return [str(item) for item in self._json_dict['genres']]

    @property
    def href(self) -> str:
        """
        A link to the Web API endpoint providing full details of the album.
        """
        return str(self._json_dict['href'])

    @property
    def id(self) -> str:
        """
        The Spotify ID for the album.
        """
        return str(self._json_dict['id'])

    @property
    def images(self) -> List[ImageObject]:
        """
        The cover art for the album in various sizes, widest first.
        """
        return [ImageObject(item) for item in self._json_dict['images']]

    @property
    def label(self) -> str:
        """
        The label for the album.
        """
        return str(self._json_dict['label'])

    @property
    def name(self) -> str:
        """
        The name of the album. In case of an album takedown, the value may be
        an empty string.
        """
        return str(self._json_dict['name'])

    @property
    def popularity(self) -> int:
        """
        The popularity of the album. The value will be between 0 and 100, with
        100 being the most popular. The popularity is calculated from the
        popularity of the album’s individual tracks.
        """
        return int(self._json_dict['popularity'])

    @property
    def release_date(self) -> str:
        """
        The date the album was first released, for example “1981-12-15”.
        Depending on the precision, it might be shown as “1981” or “1981-12”.
        """
        return str(self._json_dict['release_date'])

    @property
    def release_date_precision(self) -> str:
        """
        The precision with which release_date value is known: “year”, “month”,
        or “day”.
        """
        return str(self._json_dict['release_date_precision'])

    @property
    def restrictions(self) -> Optional[AlbumRestrictionObject]:
        """
        Included in the response when a content restriction is applied. See
        Restriction Object for more details.
        """
        if value := self._json_dict.get('restrictions'):
            return AlbumRestrictionObject(value)
        return None

    @property
    def tracks(self) -> PagingObject[SimplifiedTrackObject]:
        """
        The tracks of the album.
        """
        return PagingObject(self._json_dict['tracks'], SimplifiedTrackObject)

    @property
    def type(self) -> str:
        """
        The object type: “album”.
        """
        return str(self._json_dict['type'])

    @property
    def uri(self) -> str:
        """
        The Spotify URI for the album.
        """
        return str(self._json_dict['uri'])


class AlbumRestrictionObject(SpotifyObject):
    """
    Album Restriction Object docstring...
    """

    def __repr__(self):
        return f'<AlbumRestrictionObject reason={self.reason!r}>'

    @property
    def reason(self) -> str:
        """
        The reason for the restriction. Supported values:
            market - The content item is not available in the given market.
            product - The content item is not available for the user’s
        subscription type.
            explicit - The content item is explicit and the user’s account is
        set to not play explicit content.

        Additional reasons may be added in the future.
        """
        return str(self._json_dict['reason'])


class ArtistObject(SpotifyObject):
    """
    Artist docstring
    """

    def __repr__(self):
        return f'<ArtistObject name={self.name!r}>'

    @property
    def external_urls(self) -> ExternalUrlObject:
        """
        Known external URLs for this artist.
        """
        return ExternalUrlObject(self._json_dict['external_urls'])

    @property
    def followers(self) -> FollowersObject:
        """
        Information about the followers of the artist.
        """
        return FollowersObject(self._json_dict['followers'])

    @property
    def genres(self) -> List[str]:
        """
        A list of the genres the artist is associated with. For example: "Prog
        Rock" , "Post-Grunge". (If not yet classified, the array is empty.)
        """
        return [str(item) for item in self._json_dict['genres']]

    @property
    def href(self) -> str:
        """
        A link to the Web API endpoint providing full details of the artist.
        """
        return str(self._json_dict['href'])

    @property
    def id(self) -> str:
        """
        The Spotify ID for the artist.
        """
        return str(self._json_dict['id'])

    @property
    def images(self) -> List[ImageObject]:
        """
        Images of the artist in various sizes, widest first.
        """
        return [ImageObject(item) for item in self._json_dict['images']]

    @property
    def name(self) -> str:
        """
        The name of the artist.
        """
        return str(self._json_dict['name'])

    @property
    def popularity(self) -> int:
        """
        The popularity of the artist. The value will be between 0 and 100,
        with 100 being the most popular. The artist’s popularity is calculated
        from the popularity of all the artist’s tracks.
        """
        return int(self._json_dict['popularity'])

    @property
    def type(self) -> str:
        """
        The object type: "artist"
        """
        return str(self._json_dict['type'])

    @property
    def uri(self) -> List[ImageObject]:
        """
        The Spotify URI for the artist.
        """
        return [ImageObject(item) for item in self._json_dict['uri']]


class AudioFeaturesObject(SpotifyObject):
    """
    AudioFeatures docstring..
    """

    def __repr__(self):
        return f'<AudioFeaturesObject id={self.id!r}>'

    @property
    def acousticness(self) -> float:
        """
        A confidence measure from 0.0 to 1.0 of whether the track is acoustic.
        1.0 represents high confidence the track is acoustic.
        """
        return float(self._json_dict['acousticness'])

    @property
    def analysis_url(self) -> str:
        """
        An HTTP URL to access the full audio analysis of this track. An access
        token is required to access this data.
        """
        return str(self._json_dict['analysis_url'])

    @property
    def danceability(self) -> float:
        """
        Danceability describes how suitable a track is for dancing based on a
        combination of musical elements including tempo, rhythm stability,
        beat strength, and overall regularity. A value of 0.0 is least
        danceable and 1.0 is most danceable.
        """
        return float(self._json_dict['danceability'])

    @property
    def duration_ms(self) -> int:
        """
        The duration of the track in milliseconds.
        """
        return int(self._json_dict['duration_ms'])

    @property
    def energy(self) -> float:
        """
        Energy is a measure from 0.0 to 1.0 and represents a perceptual
        measure of intensity and activity. Typically, energetic tracks feel
        fast, loud, and noisy. For example, death metal has high energy, while
        a Bach prelude scores low on the scale. Perceptual features
        contributing to this attribute include dynamic range, perceived
        loudness, timbre, onset rate, and general entropy.
        """
        return float(self._json_dict['energy'])

    @property
    def id(self) -> str:
        """
        The Spotify ID for the track.
        """
        return str(self._json_dict['id'])

    @property
    def instrumentalness(self) -> int:
        """
        Predicts whether a track contains no vocals. “Ooh” and “aah” sounds
        are treated as instrumental in this context. Rap or spoken word tracks
        are clearly “vocal”. The closer the instrumentalness value is to 1.0,
        the greater likelihood the track contains no vocal content. Values
        above 0.5 are intended to represent instrumental tracks, but
        confidence is higher as the value approaches 1.0.)
        """
        return int(self._json_dict['instrumentalness'])

    @property
    def key(self) -> int:
        """
        The key the track is in. Integers map to pitches using standard Pitch
        Class notation . E.g. 0 = C, 1 = C♯/D♭, 2 = D, and so on.
        """
        return int(self._json_dict['key'])

    @property
    def liveness(self) -> float:
        """
        Detects the presence of an audience in the recording. Higher liveness
        values represent an increased probability that the track was performed
        live. A value above 0.8 provides strong likelihood that the track is
        live.
        """
        return float(self._json_dict['liveness'])

    @property
    def loudness(self) -> float:
        """
        The overall loudness of a track in decibels (dB). Loudness values are
        averaged across the entire track and are useful for comparing relative
        loudness of tracks. Loudness is the quality of a sound that is the
        primary psychological correlate of physical strength (amplitude).
        Values typical range between -60 and 0 db.
        """
        return float(self._json_dict['loudness'])

    @property
    def mode(self) -> int:
        """
        Mode indicates the modality (major or minor) of a track, the type of
        scale from which its melodic content is derived. Major is represented
        by 1 and minor is 0.
        """
        return int(self._json_dict['mode'])

    @property
    def speechiness(self) -> float:
        """
        Speechiness detects the presence of spoken words in a track. The more
        exclusively speech-like the recording (e.g. talk show, audio book,
        poetry), the closer to 1.0 the attribute value. Values above 0.66
        describe tracks that are probably made entirely of spoken words.
        Values between 0.33 and 0.66 describe tracks that may contain both
        music and speech, either in sections or layered, including such cases
        as rap music. Values below 0.33 most likely represent music and other
        non-speech-like tracks.
        """
        return float(self._json_dict['speechiness'])

    @property
    def tempo(self) -> float:
        """
        The overall estimated tempo of a track in beats per minute (BPM). In
        musical terminology, tempo is the speed or pace of a given piece and
        derives directly from the average beat duration.
        """
        return float(self._json_dict['tempo'])

    @property
    def time_signature(self) -> int:
        """
        An estimated overall time signature of a track. The time signature
        (meter) is a notational convention to specify how many beats are in
        each bar (or measure).
        """
        return int(self._json_dict['time_signature'])

    @property
    def track_href(self) -> str:
        """
        A link to the Web API endpoint providing full details of the track.
        """
        return str(self._json_dict['track_href'])

    @property
    def type(self) -> str:
        """
        The object type: “audio_features”
        """
        return str(self._json_dict['type'])

    @property
    def uri(self) -> str:
        """
        The Spotify URI for the track.
        """
        return str(self._json_dict['uri'])

    @property
    def valence(self) -> float:
        """
        A measure from 0.0 to 1.0 describing the musical positiveness conveyed
        by a track. Tracks with high valence sound more positive (e.g. happy,
        cheerful, euphoric), while tracks with low valence sound more negative
        (e.g. sad, depressed, angry).
        """
        return float(self._json_dict['valence'])


class CategoryObject(SpotifyObject):
    """
    CategoryObject doc string....
    """

    def __repr__(self):
        return f'<CategoryObject name={self.name!r}>'

    @property
    def href(self) -> str:
        """
        A link to the Web API endpoint returning full details of the category.
        """
        return str(self._json_dict['href'])

    @property
    def icons(self) -> List[ImageObject]:
        """
        The category icon, in various sizes.
        """
        return [ImageObject(item) for item in self._json_dict['icons']]

    @property
    def id(self) -> str:
        """
        The Spotify category ID of the category.
        """
        return str(self._json_dict['id'])

    @property
    def name(self) -> str:
        """
        The name of the category.
        """
        return str(self._json_dict['name'])


class ContextObject(SpotifyObject):
    """
    ContextObject doc string....
    """

    def __repr__(self):
        return f'<ContextObject type={self.type!r}>'

    @property
    def external_urls(self) -> ExternalUrlObject:
        """
        External URLs for this context.
        """
        return ExternalUrlObject(self._json_dict['external_urls'])

    @property
    def href(self) -> str:
        """
        A link to the Web API endpoint providing full details of the track.
        """
        return str(self._json_dict['href'])

    @property
    def type(self) -> str:
        """
        The object type, e.g. “artist”, “playlist”, “album”, “show”.
        """
        return str(self._json_dict['type'])

    @property
    def uri(self) -> str:
        """
        The Spotify URI for the context.
        """
        return str(self._json_dict['uri'])


class CopyrightObject(SpotifyObject):
    """
    Copyright doc string....
    """

    def __repr__(self):
        return f'<CopyrightObject text={self.text!r},' \
               f'type={self.type!r}>'

    @property
    def text(self) -> str:
        """
        The copyright text for this content.
        """
        return str(self._json_dict['text'])

    @property
    def type(self) -> str:
        """
        The type of copyright: C = the copyright, P = the sound recording
        (performance) copyright.
        """
        return str(self._json_dict['type'])


class CurrentlyPlayingContextObject(SpotifyObject):
    """
    CurrentlyPlayingContext doc string....
    """

    def __repr__(self):
        return f'<CurrentlyPlayingContextObject device={self.device},' \
               f'repeat_state={self.repeat_state!r},' \
               f'shuffle_state={self.shuffle_state!r}>'

    @property
    def actions(self) -> DisallowsObject:
        """
        Allows to update the user interface based on which playback actions
        are available within the current context.
        """
        return DisallowsObject(self._json_dict['actions'])

    @property
    def context(self) -> Optional[ContextObject]:
        """
        A Context Object. Can be None.
        """
        if value := self._json_dict.get('context'):
            return ContextObject(value)
        return None

    @property
    def currently_playing_type(self) -> str:
        """
        The object type of the currently playing item. Can be one of track,
        episode, ad or unknown.
        """
        return str(self._json_dict['currently_playing_type'])

    @property
    def device(self) -> DeviceObject:
        """
        The device that is currently active.
        """
        return DeviceObject(self._json_dict['device'])

    @property
    def is_playing(self) -> bool:
        """
        If something is currently playing, return True.
        """
        return bool(self._json_dict['is_playing'])

    @property
    def item(self) -> Union[TrackObject, EpisodeObject, None]:
        """
        The currently playing track or episode. Can be None.
        """
        return union_parser([TrackObject, EpisodeObject, None], self._json_dict['item'])

    @property
    def progress_ms(self) -> Optional[int]:
        """
        Progress into the currently playing track or episode. Can be null.
        """
        if value := self._json_dict.get('progress_ms'):
            return int(value)
        return None

    @property
    def repeat_state(self) -> str:
        """
        off, track, context
        """
        return str(self._json_dict['repeat_state'])

    @property
    def shuffle_state(self) -> str:
        """
        If shuffle is on or off.
        """
        return str(self._json_dict['shuffle_state'])

    @property
    def timestamp(self) -> int:
        """
        Unix Millisecond Timestamp when data was fetched.
        """
        return int(self._json_dict['timestamp'])


class CurrentlyPlayingObject(SpotifyObject):
    """
    CurrentlyPlaying doc string....
    """

    def __repr__(self):
        return f'<CurrentlyPlayingObject item={self.item}>'

    @property
    def context(self) -> Optional[ContextObject]:
        """
        A Context Object. Can be None.
        """
        if value := self._json_dict.get('context'):
            return ContextObject(value)
        return None

    @property
    def currently_playing_type(self) -> str:
        """
        The object type of the currently playing item. Can be one of track,
        episode, ad or unknown.
        """
        return str(self._json_dict['currently_playing_type'])

    @property
    def is_playing(self) -> bool:
        """
        If something is currently playing, return True.
        """
        return bool(self._json_dict['is_playing'])

    @property
    def item(self) -> Union[TrackObject, EpisodeObject, None]:
        """
        The currently playing track or episode. Can be None.
        """
        return union_parser([TrackObject, EpisodeObject, None], self._json_dict['item'])

    @property
    def progress_ms(self) -> Optional[int]:
        """
        Progress into the currently playing track or episode. Can be null.
        """
        if value := self._json_dict.get('progress_ms'):
            return int(value)
        return None

    @property
    def timestamp(self) -> int:
        """
        Unix Millisecond Timestamp when data was fetched.
        """
        return int(self._json_dict['timestamp'])


class CursorObject(SpotifyObject):
    """
    CursorObject doc string..
    """

    def __repr__(self):
        return f'<CursorObject after={self.after!r}>'

    @property
    def after(self) -> str:
        """
        The cursor to use as key to find the next page of items.
        """
        return str(self._json_dict['after'])


class CursorPagingObject(SpotifyObject):
    """
    CursorPagingObject doc string...
    """

    def __repr__(self):
        return f'<CursorPagingObject items={self.items},' \
               f'limit={self.limit}, next={self.next}>'

    @property
    def cursors(self) -> CursorObject:
        """
        The cursors used to find the next set of items.
        """
        return CursorObject(self._json_dict['cursors'])

    @property
    def href(self) -> str:
        """
        A link to the Web API endpoint returning the full result of the
        request.
        """
        return str(self._json_dict['href'])

    @property
    def items(self) -> List[SpotifyObject]:
        """
        The requested data.
        """
        return [SpotifyObject(item) for item in self._json_dict['items']]

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
        URL to the next page of items. (Returns None if this is the last page)
        """
        if value := self._json_dict.get('next'):
            return str(value)
        return None

    @property
    def total(self) -> int:
        """
        Unix Millisecond Timestamp when data was fetched.
        """
        return int(self._json_dict['total'])


class DeviceObject(SpotifyObject):
    """
    DeviceObject doc string...
    """

    def __repr__(self):
        return f'<DeviceObject name={self.name!r}, id={self.id},' \
               f'type={self.type!r}>'

    @property
    def id(self) -> Optional[str]:
        """
        The device ID. This may be None.
        """
        if value := self._json_dict.get('id'):
            return str(value)
        return None

    @property
    def is_active(self) -> bool:
        """
        If this device is the currently active device.
        """
        return bool(self._json_dict['is_active'])

    @property
    def is_private_session(self) -> bool:
        """
        If this device is currently in a private session.
        """
        return bool(self._json_dict['is_private_session'])

    @property
    def is_restricted(self) -> bool:
        """
        Whether controlling this device is restricted. At present if this is
        True then no Web API commands will be accepted by this device.
        """
        return bool(self._json_dict['is_restricted'])

    @property
    def name(self) -> str:
        """
        The name of the device.
        """
        return str(self._json_dict['name'])

    @property
    def type(self) -> str:
        """
        Device type, such as “computer”, “smartphone” or “speaker”.
        """
        return str(self._json_dict['type'])

    @property
    def volume_percent(self) -> Optional[int]:
        """
        The current volume in percent. This may be None.
        """
        if value := self._json_dict.get('volume_percent'):
            return int(value)
        return None


class DevicesObject(SpotifyObject):
    """
    DevicesObject doc string...
    """

    def __repr__(self):
        return f'<DevicesObject devices={self.devices}>'

    @property
    def devices(self) -> List[DeviceObject]:
        """
        A list of 0..n Device objects
        """
        return [DeviceObject(item) for item in self._json_dict['devices']]


class DisallowsObject(SpotifyObject):
    """
    DisallowsObject doc string...
    """

    def __repr__(self):
        return f'<DisallowsObject' \
               f'interrupting_playback={self.interrupting_playback},' \
               f'pausing={self.pausing}, resuming={self.resuming},' \
               f'seeking={self.seeking},' \
               f'skipping_next={self.skipping_next},' \
               f'skipping_prev={self.skipping_prev},' \
               f'toggling_repeat_context={self.toggling_repeat_context},' \
               f'toggling_repeat_track={self.toggling_repeat_track},' \
               f'toggling_shuffle={self.toggling_shuffle},' \
               f'transferring_playback={self.transferring_playback}>'

    @property
    def interrupting_playback(self) -> Optional[bool]:
        """
        Interrupting playback. Optional field.
        """
        if value := self._json_dict.get('interrupting_playback'):
            return bool(value)
        return None

    @property
    def pausing(self) -> Optional[bool]:
        """
        Pausing. Optional field.
        """
        if value := self._json_dict.get('pausing'):
            return bool(value)
        return None

    @property
    def resuming(self) -> Optional[bool]:
        """
        Resuming. Optional field.
        """
        if value := self._json_dict.get('resuming'):
            return bool(value)
        return None

    @property
    def seeking(self) -> Optional[bool]:
        """
        Seeking playback location. Optional field.
        """
        if value := self._json_dict.get('seeking'):
            return bool(value)
        return None

    @property
    def skipping_next(self) -> Optional[bool]:
        """
        Skipping to the next context. Optional field.
        """
        if value := self._json_dict.get('skipping_next'):
            return bool(value)
        return None

    @property
    def skipping_prev(self) -> Optional[bool]:
        """
        Skipping to the previous context. Optional field.
        """
        if value := self._json_dict.get('skipping_prev'):
            return bool(value)
        return None

    @property
    def toggling_repeat_context(self) -> Optional[bool]:
        """
        Toggling repeat context flag. Optional field.
        """
        if value := self._json_dict.get('toggling_repeat_context'):
            return bool(value)
        return None

    @property
    def toggling_repeat_track(self) -> Optional[bool]:
        """
        Toggling repeat track flag. Optional field.
        """
        if value := self._json_dict.get('toggling_repeat_track'):
            return bool(value)
        return None

    @property
    def toggling_shuffle(self) -> Optional[bool]:
        """
        Toggling shuffle flag. Optional field.
        """
        if value := self._json_dict.get('toggling_shuffle'):
            return bool(value)
        return None

    @property
    def transferring_playback(self) -> Optional[bool]:
        """
        Transferring playback between devices. Optional field.
        """
        if value := self._json_dict.get('transferring_playback'):
            return bool(value)
        return None


class EpisodeObject(SpotifyObject):
    """
    EpisodeObject doc string...
    """

    def __repr__(self):
        return f'<EpisodeObject name={self.name!r}, show={self.show},' \
               f'id={self.id!r}>'

    @property
    def audio_preview_url(self) -> Optional[str]:
        """
        A URL to a 30 second preview (MP3 format) of the episode. None if not
        available.
        """
        if value := self._json_dict.get('audio_preview_url'):
            return str(value)
        return None

    @property
    def description(self) -> str:
        """
        A description of the episode.
        """
        return str(self._json_dict['description'])

    @property
    def duration_ms(self) -> int:
        """
        The episode length in milliseconds.
        """
        return int(self._json_dict['duration_ms'])

    @property
    def explicit(self) -> bool:
        """
        Whether or not the episode has explicit content (True = yes it does;
        False = no it does not OR unknown).
        """
        return bool(self._json_dict['explicit'])

    @property
    def external_urls(self) -> ExternalUrlObject:
        """
        External URLs for this episode.
        """
        return ExternalUrlObject(self._json_dict['external_urls'])

    @property
    def href(self) -> str:
        """
        A link to the Web API endpoint providing full details of the episode.
        """
        return str(self._json_dict['href'])

    @property
    def id(self) -> str:
        """
        The Spotify ID for the episode.
        """
        return str(self._json_dict['id'])

    @property
    def images(self) -> List[ImageObject]:
        """
        The cover art for the episode in various sizes, widest first.
        """
        return [ImageObject(item) for item in self._json_dict['images']]

    @property
    def is_externally_hosted(self) -> bool:
        """
        True if the episode is hosted outside of Spotify’s CDN.
        """
        return bool(self._json_dict['is_externally_hosted'])

    @property
    def is_playable(self) -> bool:
        """
        True if the episode is playable in the given market. Otherwise False.
        """
        return bool(self._json_dict['is_playable'])

    @property
    def languages(self) -> List[str]:
        """
        A list of the languages used in the episode, identified by their ISO
        639 code.
        """
        return [str(item) for item in self._json_dict['languages']]

    @property
    def name(self) -> str:
        """
        The name of the episode.
        """
        return str(self._json_dict['name'])

    @property
    def release_date(self) -> str:
        """
        The date the episode was first released, for example "1981-12-15".
        Depending on the precision, it might be shown as "1981" or "1981-12".
        """
        return str(self._json_dict['release_date'])

    @property
    def release_date_precision(self) -> str:
        """
        The precision with which release_date value is known: "year", "month",
        or "day".
        """
        return str(self._json_dict['release_date_precision'])

    @property
    def resume_point(self) -> Optional[ResumePointObject]:
        """
        The user’s most recent position in the episode. Set if the supplied
        access token is a user token and has the scope user-read-playback-
        position.
        """
        if value := self._json_dict.get('resume_point'):
            return ResumePointObject(value)
        return None

    @property
    def show(self) -> SimplifiedShowObject:
        """
        The show on which the episode belongs.
        """
        return SimplifiedShowObject(self._json_dict['show'])

    @property
    def type(self) -> str:
        """
        The object type: “episode”.
        """
        return str(self._json_dict['type'])

    @property
    def uri(self) -> str:
        """
        The Spotify URI for the episode.
        """
        return str(self._json_dict['uri'])


class ErrorObject(SpotifyObject):
    """
    ErrorObject doc string...
    """

    def __repr__(self):
        return f'<ErrorObject message={self.message!r},' \
               f'status={self.status}>'

    @property
    def message(self) -> str:
        """
        A short description of the cause of the error.
        """
        return str(self._json_dict['message'])

    @property
    def status(self) -> int:
        """
        The HTTP status code.
        """
        return int(self._json_dict['status'])


class ExplicitContentSettingsObject(SpotifyObject):
    """
    ExplicitContentSettings doc string...
    """

    def __repr__(self):
        return f'<ExplicitContentSettingsObject' \
               f'filter_enabled={self.filter_enabled},' \
               f'filter_locked={self.filter_locked}>'

    @property
    def filter_enabled(self) -> bool:
        """
        When True, indicates that explicit content should not be played.
        """
        return bool(self._json_dict['filter_enabled'])

    @property
    def filter_locked(self) -> bool:
        """
        When True, indicates that the explicit content setting is locked and
        can’t be changed by the user.
        """
        return bool(self._json_dict['filter_locked'])


class ExternalIdObject(SpotifyObject):
    """
    ExternalIdObject doc string...
    """

    def __repr__(self):
        return f'<ExternalIdObject ean={self.ean!r},' \
               f'isrc={self.isrc!r}, upc={self.upc!r}>'

    @property
    def ean(self) -> str:
        """
        International Article Number.
        """
        return str(self._json_dict['ean'])

    @property
    def isrc(self) -> str:
        """
        International Standard Recording Code.
        """
        return str(self._json_dict['isrc'])

    @property
    def upc(self) -> str:
        """
        Universal Product Code.
        """
        return str(self._json_dict['upc'])


class ExternalUrlObject(SpotifyObject):
    """
    ExternalUrlObject doc string...
    """

    def __repr__(self):
        return f'<ExternalUrlObject spotify={self.spotify!r}>'

    @property
    def spotify(self) -> str:
        """
        The Spotify URL for the object.
        """
        return str(self._json_dict['spotify'])


class FollowersObject(SpotifyObject):
    """
    FollowersObject doc string...
    """

    def __repr__(self):
        return f'<FollowersObject total={self.total}>'

    @property
    def total(self) -> int:
        """
        The total number of followers.
        """
        return int(self._json_dict['total'])


class ImageObject(SpotifyObject):
    """
    ImageObject doc string...
    """

    def __repr__(self):
        return f'<ImageObject url={self.url!r}, height={self.height},' \
               f'width={self.width}>'

    @property
    def height(self) -> Optional[int]:
        """
        The image height in pixels. If unknown: None.
        """
        if value := self._json_dict.get('height'):
            return int(value)
        return None

    @property
    def url(self) -> str:
        """
        The source URL of the image.
        """
        return str(self._json_dict['url'])

    @property
    def width(self) -> Optional[int]:
        """
        The image width in pixels. If unknown: None.
        """
        if value := self._json_dict.get('width'):
            return int(value)
        return None


class LinkedTrackObject(SpotifyObject):
    """
    LinkedTrackObject doc string...
    """

    def __repr__(self):
        return f'<LinkedTrackObject id={self.id!r}, uri={self.uri!r}>'

    @property
    def external_urls(self) -> ExternalUrlObject:
        """
        Known external URLs for this track.
        """
        return ExternalUrlObject(self._json_dict['external_urls'])

    @property
    def href(self) -> str:
        """
        A link to the Web API endpoint providing full details of the track.
        """
        return str(self._json_dict['href'])

    @property
    def id(self) -> str:
        """
        The Spotify ID for the track.
        """
        return str(self._json_dict['id'])

    @property
    def type(self) -> str:
        """
        The object type: “track”.
        """
        return str(self._json_dict['type'])

    @property
    def uri(self) -> str:
        """
        The Spotify URI for the track.
        """
        return str(self._json_dict['uri'])


class PlayHistoryObject(SpotifyObject):
    """
    PlayHistoryObject doc string...
    """

    def __repr__(self):
        return f'<PlayHistoryObject track={self.track},' \
               f'played_at={self.played_at}>'

    @property
    def context(self) -> ContextObject:
        """
        The context the track was played from.
        """
        return ContextObject(self._json_dict['context'])

    @property
    def played_at(self) -> datetime:
        """
        The date and time the track was played.
        """
        return datetime.fromisoformat(self._json_dict['played_at'])

    @property
    def track(self) -> SimplifiedTrackObject:
        """
        The track the user listened to.
        """
        return SimplifiedTrackObject(self._json_dict['track'])


class PlayErrorObject(SpotifyObject):
    """
    PlayErrorObject doc string...
    """

    def __repr__(self):
        return f'<PlayErrorObject message={self.message!r},' \
               f'reason={self.reason!r}, status={self.status}>'

    @property
    def message(self) -> str:
        """
        A short description of the cause of the error.
        """
        return str(self._json_dict['message'])

    @property
    def reason(self) -> str:
        """
        NO_PREV_TRACK - The command requires a previous track, but there is
        none in the context.
        NO_NEXT_TRACK - The command requires a next track, but there is none
        in the context.
        NO_SPECIFIC_TRACK - The requested track does not exist.
        ALREADY_PAUSED - The command requires playback to not be paused.
        NOT_PAUSED - The command requires playback to be paused.
        NOT_PLAYING_LOCALLY - The command requires playback on the local
        device.
        NOT_PLAYING_TRACK - The command requires that a track is currently
        playing.
        NOT_PLAYING_CONTEXT - The command requires that a context is currently
        playing.
        ENDLESS_CONTEXT - The shuffle command cannot be applied on an endless
        context.
        CONTEXT_DISALLOW - The command could not be performed on the context.
        ALREADY_PLAYING - The track should not be restarted if the same track
        and context is already playing, and there is a resume point.
        RATE_LIMITED - The user is rate limited due to too frequent track
        play, also known as cat-on-the-keyboard spamming.
        REMOTE_CONTROL_DISALLOW - The context cannot be remote-controlled.
        DEVICE_NOT_CONTROLLABLE - Not possible to remote control the device.
        VOLUME_CONTROL_DISALLOW - Not possible to remote control the device’s
        volume.
        NO_ACTIVE_DEVICE - Requires an active device and the user has none.
        PREMIUM_REQUIRED - The request is prohibited for non-premium users.
        UNKNOWN - Certain actions are restricted because of unknown reasons.
        """
        return str(self._json_dict['reason'])

    @property
    def status(self) -> int:
        """
        The HTTP status code. Either 404 NOT FOUND or 403 FORBIDDEN.
        """
        return int(self._json_dict['status'])


class PlaylistObject(SpotifyObject):
    """
    PlayListObject doc string...
    """

    def __repr__(self):
        return f'<PlaylistObject name={self.name!r}, id={self.id!r},' \
               f'tracks={self.tracks}>'

    @property
    def collaborative(self) -> bool:
        """
        True if the owner allows other users to modify the playlist
        """
        return bool(self._json_dict['collaborative'])

    @property
    def description(self) -> Optional[str]:
        """
        The playlist description. Only returned for modified, verified
        playlists, otherwise None.
        """
        if value := self._json_dict.get('description'):
            return str(value)
        return None

    @property
    def external_urls(self) -> ExternalUrlObject:
        """
        Known external URLs for this playlist.
        """
        return ExternalUrlObject(self._json_dict['external_urls'])

    @property
    def followers(self) -> FollowersObject:
        """
        Information about the followers of the playlist.
        """
        return FollowersObject(self._json_dict['followers'])

    @property
    def href(self) -> str:
        """
        A link to the Web API endpoint providing full details of the playlist.
        """
        return str(self._json_dict['href'])

    @property
    def id(self) -> str:
        """
        The Spotify ID for the playlist.
        """
        return str(self._json_dict['id'])

    @property
    def images(self) -> List[ImageObject]:
        """
        Images for the playlist. The array may be empty or contain up to three
        images. The images are returned by size in descending order. Note: If
        returned, the source URL for the image (url) is temporary and will
        expire in less than a day.
        """
        return [ImageObject(item) for item in self._json_dict['images']]

    @property
    def name(self) -> str:
        """
        The name of the playlist.
        """
        return str(self._json_dict['name'])

    @property
    def owner(self) -> PublicUserObject:
        """
        The user who owns the playlist
        """
        return PublicUserObject(self._json_dict['owner'])

    @property
    def public(self) -> Optional[bool]:
        """
        The playlist’s public/private status: True the playlist is public,
        False the playlist is private, None the playlist status is not
        relevant.
        """
        if value := self._json_dict.get('public'):
            return bool(value)
        return None

    @property
    def snapshot_id(self) -> str:
        """
        The version identifier for the current playlist. Can be supplied in
        other requests to target a specific playlist version.
        """
        return str(self._json_dict['snapshot_id'])

    @property
    def tracks(self) -> List[Optional[PlaylistTrackObject]]:
        """
        Information about the tracks of the playlist. Note, a track object may
        be None. This can happen if a track is no longer available.
        """
        return [Optional[PlaylistTrackObject](item) for item in self._json_dict['tracks']]

    @property
    def type(self) -> str:
        """
        The object type: “playlist”.
        """
        return str(self._json_dict['type'])

    @property
    def uri(self) -> str:
        """
        The Spotify URI for the playlist.
        """
        return str(self._json_dict['uri'])


class PlaylistTrackObject(SpotifyObject):
    """
    PlayListTrackObject doc string...
    """

    def __repr__(self):
        return f'<PlaylistTrackObject track={self.track}>'

    @property
    def added_at(self) -> Optional[datetime]:
        """
        The date and time the track or episode was added. Note that some very
        old playlists may return None in this field.
        """
        if value := self._json_dict.get('added_at'):
            return datetime.fromisoformat(value)
        return None

    @property
    def added_by(self) -> Optional[PublicUserObject]:
        """
        The Spotify user who added the track or episode. Note that some very
        old playlists may return None in this field.
        """
        if value := self._json_dict.get('added_by'):
            return PublicUserObject(value)
        return None

    @property
    def is_local(self) -> bool:
        """
        Whether this track or episode is a local file or not.
        """
        return bool(self._json_dict['is_local'])

    @property
    def track(self) -> Union[TrackObject, EpisodeObject]:
        """
        Information about the track or episode.
        """
        return union_parser([TrackObject, EpisodeObject], self._json_dict['track'])


class PlaylistTracksRefObject(SpotifyObject):
    """
    PlaylistTracksRefObject doc string...
    """

    def __repr__(self):
        return f'<PlaylistTracksRefObject href={self.href!r}>'

    @property
    def href(self) -> str:
        """
        A link to the Web API endpoint where full details of the playlist’s
        tracks can be retrieved.
        """
        return str(self._json_dict['href'])

    @property
    def total(self) -> int:
        """
        Number of tracks in the playlist.
        """
        return int(self._json_dict['total'])


class PrivateUserObject(SpotifyObject):
    """
    PrivateUserObject doc string...
    """

    def __repr__(self):
        return f'<PrivateUserObject display_name={self.display_name},' \
               f'email={self.email}, id={self.id!r}>'

    @property
    def country(self) -> str:
        """
        The country of the user, as set in the user’s account profile. An ISO
        3166-1 alpha-2 country code. This field is only available when the
        current user has granted access to the user-read-private scope.
        """
        return str(self._json_dict['country'])

    @property
    def display_name(self) -> Optional[str]:
        """
        The name displayed on the user’s profile. None if not available.
        """
        if value := self._json_dict.get('display_name'):
            return str(value)
        return None

    @property
    def email(self) -> Optional[str]:
        """
        The user’s email address, as entered by the user when creating their
        account. Important! This email address is unverified; there is no
        proof that it actually belongs to the user. This field is only
        available when the current user has granted access to the user-read-
        email scope.
        """
        if value := self._json_dict.get('email'):
            return str(value)
        return None

    @property
    def explicit_content(self) -> Optional[ExplicitContentSettingsObject]:
        """
        The user’s explicit content settings. This field is only available
        when the current user has granted access to the user-read-private
        scope.
        """
        if value := self._json_dict.get('explicit_content'):
            return ExplicitContentSettingsObject(value)
        return None

    @property
    def external_urls(self) -> ExternalUrlObject:
        """
        Known external URLs for this user.
        """
        return ExternalUrlObject(self._json_dict['external_urls'])

    @property
    def followers(self) -> FollowersObject:
        """
        Information about the followers of the user.
        """
        return FollowersObject(self._json_dict['followers'])

    @property
    def href(self) -> str:
        """
        A link to the Web API endpoint for this user.
        """
        return str(self._json_dict['href'])

    @property
    def id(self) -> str:
        """
        The Spotify user ID for the user.
        """
        return str(self._json_dict['id'])

    @property
    def images(self) -> List[ImageObject]:
        """
        The user’s profile image.
        """
        return [ImageObject(item) for item in self._json_dict['images']]

    @property
    def product(self) -> Optional[str]:
        """
        The user’s Spotify subscription level: “premium”, “free”, etc. (The
        subscription level “open” can be considered the same as “free”.) This
        field is only available when the current user has granted access to
        the user-read-private scope.
        """
        if value := self._json_dict.get('product'):
            return str(value)
        return None

    @property
    def type(self) -> str:
        """
        The object type: “user”.
        """
        return str(self._json_dict['type'])

    @property
    def uri(self) -> str:
        """
        The Spotify URI for the user.
        """
        return str(self._json_dict['uri'])


class PublicUserObject(SpotifyObject):
    """
    PublicUserObject doc string...
    """

    def __repr__(self):
        return f'<PublicUserObject display_name={self.display_name},' \
               f'id={self.id!r}>'

    @property
    def display_name(self) -> Optional[str]:
        """
        The name displayed on the user’s profile. None if not available.
        """
        if value := self._json_dict.get('display_name'):
            return str(value)
        return None

    @property
    def external_urls(self) -> ExternalUrlObject:
        """
        Known external URLs for this user.
        """
        return ExternalUrlObject(self._json_dict['external_urls'])

    @property
    def followers(self) -> FollowersObject:
        """
        Information about the followers of this user.
        """
        return FollowersObject(self._json_dict['followers'])

    @property
    def href(self) -> str:
        """
        A link to the Web API endpoint for this user.
        """
        return str(self._json_dict['href'])

    @property
    def id(self) -> str:
        """
        The Spotify user ID for this user.
        """
        return str(self._json_dict['id'])

    @property
    def images(self) -> List[ImageObject]:
        """
        The user’s profile image.
        """
        return [ImageObject(item) for item in self._json_dict['images']]

    @property
    def product(self) -> Optional[str]:
        """
        The user’s Spotify subscription level: “premium”, “free”, etc. (The
        subscription level “open” can be considered the same as “free”.) This
        field is only available when the current user has granted access to
        the user-read-private scope.
        """
        if value := self._json_dict.get('product'):
            return str(value)
        return None

    @property
    def type(self) -> str:
        """
        The object type: “user”.
        """
        return str(self._json_dict['type'])

    @property
    def uri(self) -> str:
        """
        The Spotify URI for the user.
        """
        return str(self._json_dict['uri'])


class RecommendationSeedObject(SpotifyObject):
    """
    RecommendationSeedObject doc string...
    """

    def __repr__(self):
        return f'<RecommendationSeedObject id={self.id!r},' \
               f'type={self.type!r}>'

    @property
    def after_filtering_size(self) -> int:
        """
        The number of tracks available after min_* and max_* filters have been
        applied.
        """
        return int(self._json_dict['after_filtering_size'])

    @property
    def after_relinking_size(self) -> int:
        """
        The number of tracks available after relinking for regional
        availability.
        """
        return int(self._json_dict['after_relinking_size'])

    @property
    def href(self) -> str:
        """
        A link to the full track or artist data for this seed. For tracks this
        will be a link to a Track Object. For artists a link to an Artist
        Object. For genre seeds, this value will be None.
        """
        return str(self._json_dict['href'])

    @property
    def id(self) -> str:
        """
        The id used to select this seed. This will be the same as the string
        used in the seed_artists, seed_tracks or seed_genres parameter.
        """
        return str(self._json_dict['id'])

    @property
    def initial_pool_size(self) -> int:
        """
        The number of recommended tracks available for this seed.
        """
        return int(self._json_dict['initial_pool_size'])

    @property
    def type(self) -> str:
        """
        The entity type of this seed. One of artist, track or genre.
        """
        return str(self._json_dict['type'])


class RecommendationsObject(SpotifyObject):
    """
    RecommendationsObject doc string...
    """

    def __repr__(self):
        return f'<RecommendationsObject seeds={self.seeds},' \
               f'tracks={self.tracks}>'

    @property
    def seeds(self) -> List[RecommendationSeedObject]:
        """
        A list of recommendation seed objects.
        """
        return [RecommendationSeedObject(item) for item in self._json_dict['seeds']]

    @property
    def tracks(self) -> List[SimplifiedTrackObject]:
        """
        A list of simplified track objects ordered according to the parameters
        supplied.
        """
        return [SimplifiedTrackObject(item) for item in self._json_dict['tracks']]


class ResumePointObject(SpotifyObject):
    """
    ResumePointObject doc string...
    """

    def __repr__(self):
        return f'<ResumePointObject fully_played={self.fully_played},' \
               f'resume_position_ms={self.resume_position_ms}>'

    @property
    def fully_played(self) -> bool:
        """
        Whether or not the episode has been fully played by the user.
        """
        return bool(self._json_dict['fully_played'])

    @property
    def resume_position_ms(self) -> int:
        """
        The user’s most recent position in the episode in milliseconds.
        """
        return int(self._json_dict['resume_position_ms'])


class SavedAlbumObject(SpotifyObject):
    """
    SavedAlbumObject doc string...
    """

    def __repr__(self):
        return f'<SavedAlbumObject album={self.album},' \
               f'added_at={self.added_at}>'

    @property
    def added_at(self) -> datetime:
        """
        The date and time the album was saved Timestamps are returned in ISO
        8601 format as Coordinated Universal Time (UTC) with a zero offset:
        YYYY-MM-DDTHH:MM:SSZ as datetime objects.
        """
        return datetime.fromisoformat(self._json_dict['added_at'])

    @property
    def album(self) -> AlbumObject:
        """
        Information about the album.
        """
        return AlbumObject(self._json_dict['album'])


class SavedEpisodeObject(SpotifyObject):
    """
    SavedEpisodeObject doc string...
    """

    def __repr__(self):
        return f'<SavedEpisodeObject episode={self.episode},' \
               f'added_at={self.added_at}>'

    @property
    def added_at(self) -> datetime:
        """
        The date and time the episode was saved Timestamps are returned in ISO
        8601 format as Coordinated Universal Time (UTC) with a zero offset:
        YYYY-MM-DDTHH:MM:SSZ as datetime objects.
        """
        return datetime.fromisoformat(self._json_dict['added_at'])

    @property
    def episode(self) -> EpisodeObject:
        """
        Information about the episode.
        """
        return EpisodeObject(self._json_dict['episode'])


class SavedShowObject(SpotifyObject):
    """
    SavedShowObject doc string...
    """

    def __repr__(self):
        return f'<SavedShowObject show={self.show},' \
               f'added_at={self.added_at}>'

    @property
    def added_at(self) -> datetime:
        """
        The date and time the show was saved Timestamps are returned in ISO
        8601 format as Coordinated Universal Time (UTC) with a zero offset:
        YYYY-MM-DDTHH:MM:SSZ as datetime objects.
        """
        return datetime.fromisoformat(self._json_dict['added_at'])

    @property
    def show(self) -> SimplifiedShowObject:
        """
        Information about the show.
        """
        return SimplifiedShowObject(self._json_dict['show'])


class SavedTrackObject(SpotifyObject):
    """
    SavedTrackObject doc string...
    """

    def __repr__(self):
        return f'<SavedTrackObject track={self.track},' \
               f'added_at={self.added_at}>'

    @property
    def added_at(self) -> datetime:
        """
        The date and time the track was saved Timestamps are returned in ISO
        8601 format as Coordinated Universal Time (UTC) with a zero offset:
        YYYY-MM-DDTHH:MM:SSZ as datetime objects.
        """
        return datetime.fromisoformat(self._json_dict['added_at'])

    @property
    def track(self) -> TrackObject:
        """
        Information about the track.
        """
        return TrackObject(self._json_dict['track'])


class ShowObject(SpotifyObject):
    """
    ShowObject doc string...
    """

    def __repr__(self):
        return f'<ShowObject name={self.name!r}, id={self.id!r},' \
               f'media_type={self.media_type!r}>'

    @property
    def available_markets(self) -> List[str]:
        """
        A list of the countries in which the show can be played, identified by
        their ISO 3166-1 alpha-2 code.
        """
        return [str(item) for item in self._json_dict['available_markets']]

    @property
    def copyrights(self) -> List[CopyrightObject]:
        """
        The copyright statement of the show.
        """
        return [CopyrightObject(item) for item in self._json_dict['copyrights']]

    @property
    def description(self) -> str:
        """
        A description of the show.
        """
        return str(self._json_dict['description'])

    @property
    def episodes(self) -> List[SimplifiedEpisodeObject]:
        """
        A list of the show’s episodes.
        """
        return [SimplifiedEpisodeObject(item) for item in self._json_dict['episodes']]

    @property
    def explicit(self) -> bool:
        """
        Whether or not the show has explicit content (True = yes it does;
        False = no it does not OR unknown).
        """
        return bool(self._json_dict['explicit'])

    @property
    def external_urls(self) -> ExternalUrlObject:
        """
        External URLs for this show.
        """
        return ExternalUrlObject(self._json_dict['external_urls'])

    @property
    def href(self) -> str:
        """
        A link to the Web API endpoint providing full details of the show.
        """
        return str(self._json_dict['href'])

    @property
    def id(self) -> str:
        """
        The Spotify ID for the show.
        """
        return str(self._json_dict['id'])

    @property
    def images(self) -> List[ImageObject]:
        """
        The cover art for the show in various sizes, widest first.
        """
        return [ImageObject(item) for item in self._json_dict['images']]

    @property
    def is_externally_hosted(self) -> Optional[bool]:
        """
        True if the show is hosted outside of Spotify’s CDN. This may be None
        in some cases.
        """
        if value := self._json_dict.get('is_externally_hosted'):
            return bool(value)
        return None

    @property
    def languages(self) -> List[str]:
        """
        A list of the languages used in the show, identified by their ISO 639
        code.
        """
        return [str(item) for item in self._json_dict['languages']]

    @property
    def media_type(self) -> str:
        """
        The media type of the show.
        """
        return str(self._json_dict['media_type'])

    @property
    def name(self) -> str:
        """
        The name of the show.
        """
        return str(self._json_dict['name'])

    @property
    def publisher(self) -> str:
        """
        The publisher of the show.
        """
        return str(self._json_dict['publisher'])

    @property
    def type(self) -> str:
        """
        The object type: “show”.
        """
        return str(self._json_dict['type'])

    @property
    def uri(self) -> str:
        """
        The Spotify URI for the show.
        """
        return str(self._json_dict['uri'])


class SimplifiedAlbumObject(SpotifyObject):
    """
    SimplifiedAlbumObject Doc String.
    """

    def __repr__(self):
        return f'<SimplifiedAlbumObject name={self.name!r},' \
               f'artists={self.artists}, id={self.id!r}>'

    @property
    def album_group(self) -> str:
        """
        The field is present when getting an artist’s albums. Possible values
        are “album”, “single”, “compilation”, “appears_on”. Compare to
        album_type this field represents relationship between the artist and
        the album.
        """
        return str(self._json_dict['album_group'])

    @property
    def album_type(self) -> str:
        """
        The type of the album: album, single, or compilation.
        """
        return str(self._json_dict['album_type'])

    @property
    def artists(self) -> List[SimplifiedArtistObject]:
        """
        The artists of the album. Each artist object includes a link in href
        to more detailed information about the artist.
        """
        return [SimplifiedArtistObject(item) for item in self._json_dict['artists']]

    @property
    def available_markets(self) -> List[str]:
        """
        The markets in which the album is available: ISO 3166-1 alpha-2
        country codes. Note that an album is considered available in a market
        when at least 1 of its tracks is available in that market.
        """
        return [str(item) for item in self._json_dict['available_markets']]

    @property
    def external_urls(self) -> ExternalUrlObject:
        """
        Known external URLs for this album.
        """
        return ExternalUrlObject(self._json_dict['external_urls'])

    @property
    def href(self) -> str:
        """
        A link to the Web API endpoint providing full details of the album.
        """
        return str(self._json_dict['href'])

    @property
    def id(self) -> str:
        """
        The Spotify ID for the album.
        """
        return str(self._json_dict['id'])

    @property
    def images(self) -> List[ImageObject]:
        """
        The cover art for the album in various sizes, widest first.
        """
        return [ImageObject(item) for item in self._json_dict['images']]

    @property
    def name(self) -> str:
        """
        The name of the album. In case of an album takedown, the value may be
        an empty string.
        """
        return str(self._json_dict['name'])

    @property
    def release_date(self) -> str:
        """
        The date the album was first released, for example “1981-12-15”.
        Depending on the precision, it might be shown as “1981” or “1981-12”.
        """
        return str(self._json_dict['release_date'])

    @property
    def release_date_precision(self) -> str:
        """
        The precision with which release_date value is known: “year”, “month”,
        or “day”.
        """
        return str(self._json_dict['release_date_precision'])

    @property
    def restrictions(self) -> Optional[AlbumRestrictionObject]:
        """
        Included in the response when a content restriction is applied. See
        Restriction Object for more details.
        """
        if value := self._json_dict.get('restrictions'):
            return AlbumRestrictionObject(value)
        return None

    @property
    def type(self) -> str:
        """
        The object type: “album”.
        """
        return str(self._json_dict['type'])

    @property
    def uri(self) -> str:
        """
        The Spotify URI for the album.
        """
        return str(self._json_dict['uri'])


class SimplifiedArtistObject(SpotifyObject):
    """
    Artist docstring
    """

    def __repr__(self):
        return f'<SimplifiedArtistObject name={self.name!r},' \
               f'id={self.id!r}>'

    @property
    def external_urls(self) -> ExternalUrlObject:
        """
        Known external URLs for this artist.
        """
        return ExternalUrlObject(self._json_dict['external_urls'])

    @property
    def href(self) -> str:
        """
        A link to the Web API endpoint providing full details of the artist.
        """
        return str(self._json_dict['href'])

    @property
    def id(self) -> str:
        """
        The Spotify ID for the artist.
        """
        return str(self._json_dict['id'])

    @property
    def name(self) -> str:
        """
        The name of the artist.
        """
        return str(self._json_dict['name'])

    @property
    def type(self) -> str:
        """
        The object type: "artist".
        """
        return str(self._json_dict['type'])

    @property
    def uri(self) -> str:
        """
        TThe Spotify URI for the artist.
        """
        return str(self._json_dict['uri'])


class SimplifiedEpisodeObject(SpotifyObject):
    """
    SimplifiedEpisodeObject doc string...
    """

    def __repr__(self):
        return f'<SimplifiedEpisodeObject name={self.name!r},' \
               f'show={self.show}, id={self.id!r}>'

    @property
    def audio_preview_url(self) -> Optional[str]:
        """
        A URL to a 30 second preview (MP3 format) of the episode. None if not
        available.
        """
        if value := self._json_dict.get('audio_preview_url'):
            return str(value)
        return None

    @property
    def description(self) -> str:
        """
        A description of the episode.
        """
        return str(self._json_dict['description'])

    @property
    def duration_ms(self) -> int:
        """
        The episode length in milliseconds.
        """
        return int(self._json_dict['duration_ms'])

    @property
    def explicit(self) -> bool:
        """
        Whether or not the episode has explicit content (True = yes it does;
        False = no it does not OR unknown).
        """
        return bool(self._json_dict['explicit'])

    @property
    def external_urls(self) -> ExternalUrlObject:
        """
        External URLs for this episode.
        """
        return ExternalUrlObject(self._json_dict['external_urls'])

    @property
    def href(self) -> str:
        """
        A link to the Web API endpoint providing full details of the episode.
        """
        return str(self._json_dict['href'])

    @property
    def id(self) -> str:
        """
        The Spotify ID for the episode.
        """
        return str(self._json_dict['id'])

    @property
    def images(self) -> List[ImageObject]:
        """
        The cover art for the episode in various sizes, widest first.
        """
        return [ImageObject(item) for item in self._json_dict['images']]

    @property
    def is_externally_hosted(self) -> bool:
        """
        True if the episode is hosted outside of Spotify’s CDN.
        """
        return bool(self._json_dict['is_externally_hosted'])

    @property
    def is_playable(self) -> bool:
        """
        True if the episode is playable in the given market. Otherwise False.
        """
        return bool(self._json_dict['is_playable'])

    @property
    def languages(self) -> List[str]:
        """
        A list of the languages used in the episode, identified by their ISO
        639 code.
        """
        return [str(item) for item in self._json_dict['languages']]

    @property
    def name(self) -> str:
        """
        The name of the episode.
        """
        return str(self._json_dict['name'])

    @property
    def release_date(self) -> str:
        """
        The date the episode was first released, for example "1981-12-15".
        Depending on the precision, it might be shown as "1981" or "1981-12".
        """
        return str(self._json_dict['release_date'])

    @property
    def release_date_precision(self) -> str:
        """
        The precision with which release_date value is known: "year", "month",
        or "day".
        """
        return str(self._json_dict['release_date_precision'])

    @property
    def resume_point(self) -> Optional[ResumePointObject]:
        """
        The user’s most recent position in the episode. Set if the supplied
        access token is a user token and has the scope user-read-playback-
        position.
        """
        if value := self._json_dict.get('resume_point'):
            return ResumePointObject(value)
        return None

    @property
    def show(self) -> SimplifiedShowObject:
        """
        The show on which the episode belongs.
        """
        return SimplifiedShowObject(self._json_dict['show'])

    @property
    def type(self) -> str:
        """
        The object type: “episode”.
        """
        return str(self._json_dict['type'])

    @property
    def uri(self) -> str:
        """
        The Spotify URI for the episode.
        """
        return str(self._json_dict['uri'])


class SimplifiedPlaylistObject(SpotifyObject):
    """
    SimplifiedPlayListObject doc string...
    """

    def __repr__(self):
        return f'<SimplifiedPlaylistObject name={self.name!r},' \
               f'id={self.id!r}>'

    @property
    def collaborative(self) -> bool:
        """
        True if the owner allows other users to modify the playlist
        """
        return bool(self._json_dict['collaborative'])

    @property
    def description(self) -> Optional[str]:
        """
        The playlist description. Only returned for modified, verified
        playlists, otherwise None.
        """
        if value := self._json_dict.get('description'):
            return str(value)
        return None

    @property
    def external_urls(self) -> ExternalUrlObject:
        """
        Known external URLs for this playlist.
        """
        return ExternalUrlObject(self._json_dict['external_urls'])

    @property
    def href(self) -> str:
        """
        A link to the Web API endpoint providing full details of the playlist.
        """
        return str(self._json_dict['href'])

    @property
    def id(self) -> str:
        """
        The Spotify ID for the playlist.
        """
        return str(self._json_dict['id'])

    @property
    def images(self) -> List[ImageObject]:
        """
        Images for the playlist. The array may be empty or contain up to three
        images. The images are returned by size in descending order. Note: If
        returned, the source URL for the image (url) is temporary and will
        expire in less than a day.
        """
        return [ImageObject(item) for item in self._json_dict['images']]

    @property
    def name(self) -> str:
        """
        The name of the playlist.
        """
        return str(self._json_dict['name'])

    @property
    def owner(self) -> PublicUserObject:
        """
        The user who owns the playlist
        """
        return PublicUserObject(self._json_dict['owner'])

    @property
    def public(self) -> Optional[bool]:
        """
        The playlist’s public/private status: True the playlist is public,
        False the playlist is private, None the playlist status is not
        relevant.
        """
        if value := self._json_dict.get('public'):
            return bool(value)
        return None

    @property
    def snapshot_id(self) -> str:
        """
        The version identifier for the current playlist. Can be supplied in
        other requests to target a specific playlist version.
        """
        return str(self._json_dict['snapshot_id'])

    @property
    def tracks(self) -> Optional[PlaylistTracksRefObject]:
        """
        Information about the tracks of the playlist. Note, a track object may
        be None. This can happen if a track is no longer available.
        """
        if value := self._json_dict.get('tracks'):
            return PlaylistTracksRefObject(value)
        return None

    @property
    def type(self) -> str:
        """
        The object type: “playlist”.
        """
        return str(self._json_dict['type'])

    @property
    def uri(self) -> str:
        """
        The Spotify URI for the playlist.
        """
        return str(self._json_dict['uri'])


class SimplifiedShowObject(SpotifyObject):
    """
    ShowObject doc string...
    """

    def __repr__(self):
        return f'<SimplifiedShowObject name={self.name!r},' \
               f'id={self.id!r}, media_type={self.media_type!r}>'

    @property
    def available_markets(self) -> List[str]:
        """
        A list of the countries in which the show can be played, identified by
        their ISO 3166-1 alpha-2 code.
        """
        return [str(item) for item in self._json_dict['available_markets']]

    @property
    def copyrights(self) -> List[CopyrightObject]:
        """
        The copyright statement of the show.
        """
        return [CopyrightObject(item) for item in self._json_dict['copyrights']]

    @property
    def description(self) -> str:
        """
        A description of the show.
        """
        return str(self._json_dict['description'])

    @property
    def explicit(self) -> bool:
        """
        Whether or not the show has explicit content (True = yes it does;
        False = no it does not OR unknown).
        """
        return bool(self._json_dict['explicit'])

    @property
    def external_urls(self) -> ExternalUrlObject:
        """
        External URLs for this show.
        """
        return ExternalUrlObject(self._json_dict['external_urls'])

    @property
    def href(self) -> str:
        """
        A link to the Web API endpoint providing full details of the show.
        """
        return str(self._json_dict['href'])

    @property
    def id(self) -> str:
        """
        The Spotify ID for the show.
        """
        return str(self._json_dict['id'])

    @property
    def images(self) -> List[ImageObject]:
        """
        The cover art for the show in various sizes, widest first.
        """
        return [ImageObject(item) for item in self._json_dict['images']]

    @property
    def is_externally_hosted(self) -> Optional[bool]:
        """
        True if the show is hosted outside of Spotify’s CDN. This may be None
        in some cases.
        """
        if value := self._json_dict.get('is_externally_hosted'):
            return bool(value)
        return None

    @property
    def languages(self) -> List[str]:
        """
        A list of the languages used in the show, identified by their ISO 639
        code.
        """
        return [str(item) for item in self._json_dict['languages']]

    @property
    def media_type(self) -> str:
        """
        The media type of the show.
        """
        return str(self._json_dict['media_type'])

    @property
    def name(self) -> str:
        """
        The name of the show.
        """
        return str(self._json_dict['name'])

    @property
    def publisher(self) -> str:
        """
        The publisher of the show.
        """
        return str(self._json_dict['publisher'])

    @property
    def type(self) -> str:
        """
        The object type: “show”.
        """
        return str(self._json_dict['type'])

    @property
    def uri(self) -> str:
        """
        The Spotify URI for the show.
        """
        return str(self._json_dict['uri'])


class SimplifiedTrackObject(SpotifyObject):
    """
    SimplifiedTrackObject doc string...
    """

    def __repr__(self):
        return f'<SimplifiedTrackObject name={self.name!r},' \
               f'id={self.id!r}, artists={self.artists}>'

    @property
    def artists(self) -> List[SimplifiedArtistObject]:
        """
        The artists who performed the track. Each artist object includes a
        link in href to more detailed information about the artist.
        """
        return [SimplifiedArtistObject(item) for item in self._json_dict['artists']]

    @property
    def available_markets(self) -> List[str]:
        """
        A list of the countries in which the track can be played, identified
        by their ISO 3166-1 alpha-2 code.
        """
        return [str(item) for item in self._json_dict['available_markets']]

    @property
    def disc_number(self) -> int:
        """
        The disc number (usually 1 unless the album consists of more than one
        disc).
        """
        return int(self._json_dict['disc_number'])

    @property
    def duration_ms(self) -> int:
        """
        The track length in milliseconds.
        """
        return int(self._json_dict['duration_ms'])

    @property
    def explicit(self) -> bool:
        """
        Whether or not the track has explicit lyrics (True = yes it does;
        False = no it does not OR unknown).
        """
        return bool(self._json_dict['explicit'])

    @property
    def external_urls(self) -> ExternalUrlObject:
        """
        External URLs for this track.
        """
        return ExternalUrlObject(self._json_dict['external_urls'])

    @property
    def href(self) -> str:
        """
        A link to the Web API endpoint providing full details of the track.
        """
        return str(self._json_dict['href'])

    @property
    def id(self) -> str:
        """
        The Spotify ID for the track.
        """
        return str(self._json_dict['id'])

    @property
    def is_local(self) -> bool:
        """
        Whether or not the track is from a local file.
        """
        return bool(self._json_dict['is_local'])

    @property
    def is_playable(self) -> Optional[bool]:
        """
        Part of the response when Track Relinking is applied. If True , the
        track is playable in the given market. Otherwise False.
        """
        if value := self._json_dict.get('is_playable'):
            return bool(value)
        return None

    @property
    def linked_from(self) -> LinkedTrackObject:
        """
        Part of the response when Track Relinking is applied and is only part
        of the response if the track linking, in fact, exists. The requested
        track has been replaced with a different track. The track in the
        linked_from object contains information about the originally requested
        track.
        """
        return LinkedTrackObject(self._json_dict['linked_from'])

    @property
    def name(self) -> str:
        """
        The name of the track.
        """
        return str(self._json_dict['name'])

    @property
    def preview_url(self) -> str:
        """
        A URL to a 30 second preview (MP3 format) of the track.
        """
        return str(self._json_dict['preview_url'])

    @property
    def restrictions(self) -> TrackRestrictionObject:
        """
        Included in the response when a content restriction is applied. See
        Restriction Object for more details.
        """
        return TrackRestrictionObject(self._json_dict['restrictions'])

    @property
    def track_number(self) -> int:
        """
        The number of the track. If an album has several discs, the track
        number is the number on the specified disc.
        """
        return int(self._json_dict['track_number'])

    @property
    def type(self) -> str:
        """
        The object type: “track”.
        """
        return str(self._json_dict['type'])

    @property
    def uri(self) -> str:
        """
        The Spotify URI for the track.
        """
        return str(self._json_dict['uri'])


class TrackObject(SpotifyObject):
    """
    TrackObject doc string...
    """

    def __repr__(self):
        return f'<TrackObject name={self.name!r}, id={self.id!r},' \
               f'artists={self.artists}>'

    @property
    def album(self) -> SimplifiedAlbumObject:
        """
        The album on which the track appears. The album object includes a link
        in href to full information about the album.
        """
        return SimplifiedAlbumObject(self._json_dict['album'])

    @property
    def artists(self) -> List[SimplifiedArtistObject]:
        """
        The artists who performed the track. Each artist object includes a
        link in href to more detailed information about the artist.
        """
        return [SimplifiedArtistObject(item) for item in self._json_dict['artists']]

    @property
    def available_markets(self) -> List[str]:
        """
        A list of the countries in which the track can be played, identified
        by their ISO 3166-1 alpha-2 code.
        """
        return [str(item) for item in self._json_dict['available_markets']]

    @property
    def disc_number(self) -> int:
        """
        The disc number (usually 1 unless the album consists of more than one
        disc).
        """
        return int(self._json_dict['disc_number'])

    @property
    def duration_ms(self) -> int:
        """
        The track length in milliseconds.
        """
        return int(self._json_dict['duration_ms'])

    @property
    def explicit(self) -> bool:
        """
        Whether or not the track has explicit lyrics (True = yes it does;
        False = no it does not OR unknown).
        """
        return bool(self._json_dict['explicit'])

    @property
    def external_ids(self) -> ExternalIdObject:
        """
        Known external IDs for the track
        """
        return ExternalIdObject(self._json_dict['external_ids'])

    @property
    def external_urls(self) -> ExternalUrlObject:
        """
        External URLs for this track.
        """
        return ExternalUrlObject(self._json_dict['external_urls'])

    @property
    def href(self) -> str:
        """
        A link to the Web API endpoint providing full details of the track.
        """
        return str(self._json_dict['href'])

    @property
    def id(self) -> str:
        """
        The Spotify ID for the track.
        """
        return str(self._json_dict['id'])

    @property
    def is_local(self) -> bool:
        """
        Whether or not the track is from a local file.
        """
        return bool(self._json_dict['is_local'])

    @property
    def is_playable(self) -> Optional[bool]:
        """
        Part of the response when Track Relinking is applied. If True , the
        track is playable in the given market. Otherwise False.
        """
        if value := self._json_dict.get('is_playable'):
            return bool(value)
        return None

    @property
    def linked_from(self) -> LinkedTrackObject:
        """
        Part of the response when Track Relinking is applied and is only part
        of the response if the track linking, in fact, exists. The requested
        track has been replaced with a different track. The track in the
        linked_from object contains information about the originally requested
        track.
        """
        return LinkedTrackObject(self._json_dict['linked_from'])

    @property
    def name(self) -> str:
        """
        The name of the track.
        """
        return str(self._json_dict['name'])

    @property
    def popularity(self) -> int:
        """
        The popularity of the track. The value will be between 0 and 100, with
        100 being the most popular. \nThe popularity of a track is a value
        between 0 and 100, with 100 being the most popular. The popularity is
        calculated by algorithm and is based, in the most part, on the total
        number of plays the track has had and how recent those plays are.
        \nGenerally speaking, songs that are being played a lot now will have
        a higher popularity than songs that were played a lot in the past.
        Duplicate tracks (e.g. the same track from a single and an album) are
        rated independently. Artist and album popularity is derived
        mathematically from track popularity. Note that the popularity value
        may lag actual popularity by a few days: the value is not updated in
        real time.
        """
        return int(self._json_dict['popularity'])

    @property
    def preview_url(self) -> str:
        """
        A URL to a 30 second preview (MP3 format) of the track.
        """
        return str(self._json_dict['preview_url'])

    @property
    def restrictions(self) -> TrackRestrictionObject:
        """
        Included in the response when a content restriction is applied. See
        Restriction Object for more details.
        """
        return TrackRestrictionObject(self._json_dict['restrictions'])

    @property
    def track_number(self) -> int:
        """
        The number of the track. If an album has several discs, the track
        number is the number on the specified disc.
        """
        return int(self._json_dict['track_number'])

    @property
    def type(self) -> str:
        """
        The object type: “track”.
        """
        return str(self._json_dict['type'])

    @property
    def uri(self) -> str:
        """
        The Spotify URI for the track.
        """
        return str(self._json_dict['uri'])


class TrackRestrictionObject(SpotifyObject):
    """
    Track Restriction Object docstring...
    """

    def __repr__(self):
        return f'<TrackRestrictionObject reason={self.reason!r}>'

    @property
    def reason(self) -> str:
        """
        The reason for the restriction. Supported values:
            market - The content item is not available in the given market.
            product - The content item is not available for the user’s
        subscription type.
            explicit - The content item is explicit and the user’s account is
        set to not play explicit content.

        Additional reasons may be added in the future.
        """
        return str(self._json_dict['reason'])


class TuneableTrackObject(SpotifyObject):
    """
    TuneableTrackObject docstring..
    """

    def __repr__(self):
        return f'<TuneableTrackObject' \
               f'acousticness={self.acousticness},' \
               f'danceability={self.danceability},' \
               f'duration_ms={self.duration_ms}, energy={self.energy},' \
               f'instrumentalness={self.instrumentalness}, key={self.key},' \
               f'liveness={self.liveness}, loudness={self.loudness},' \
               f'mode={self.mode}, popularity={self.popularity},' \
               f'speechiness={self.speechiness}, tempo={self.tempo},' \
               f'time_signature={self.time_signature},' \
               f'valence={self.valence}>'

    @property
    def acousticness(self) -> float:
        """
        A confidence measure from 0.0 to 1.0 of whether the track is acoustic.
        1.0 represents high confidence the track is acoustic.
        """
        return float(self._json_dict['acousticness'])

    @property
    def danceability(self) -> float:
        """
        Danceability describes how suitable a track is for dancing based on a
        combination of musical elements including tempo, rhythm stability,
        beat strength, and overall regularity. A value of 0.0 is least
        danceable and 1.0 is most danceable.
        """
        return float(self._json_dict['danceability'])

    @property
    def duration_ms(self) -> int:
        """
        The duration of the track in milliseconds.
        """
        return int(self._json_dict['duration_ms'])

    @property
    def energy(self) -> float:
        """
        Energy is a measure from 0.0 to 1.0 and represents a perceptual
        measure of intensity and activity. Typically, energetic tracks feel
        fast, loud, and noisy. For example, death metal has high energy, while
        a Bach prelude scores low on the scale. Perceptual features
        contributing to this attribute include dynamic range, perceived
        loudness, timbre, onset rate, and general entropy.
        """
        return float(self._json_dict['energy'])

    @property
    def instrumentalness(self) -> int:
        """
        Predicts whether a track contains no vocals. “Ooh” and “aah” sounds
        are treated as instrumental in this context. Rap or spoken word tracks
        are clearly “vocal”. The closer the instrumentalness value is to 1.0,
        the greater likelihood the track contains no vocal content. Values
        above 0.5 are intended to represent instrumental tracks, but
        confidence is higher as the value approaches 1.0.)
        """
        return int(self._json_dict['instrumentalness'])

    @property
    def key(self) -> int:
        """
        The key the track is in. Integers map to pitches using standard Pitch
        Class notation . E.g. 0 = C, 1 = C♯/D♭, 2 = D, and so on.
        """
        return int(self._json_dict['key'])

    @property
    def liveness(self) -> float:
        """
        Detects the presence of an audience in the recording. Higher liveness
        values represent an increased probability that the track was performed
        live. A value above 0.8 provides strong likelihood that the track is
        live.
        """
        return float(self._json_dict['liveness'])

    @property
    def loudness(self) -> float:
        """
        The overall loudness of a track in decibels (dB). Loudness values are
        averaged across the entire track and are useful for comparing relative
        loudness of tracks. Loudness is the quality of a sound that is the
        primary psychological correlate of physical strength (amplitude).
        Values typical range between -60 and 0 db.
        """
        return float(self._json_dict['loudness'])

    @property
    def mode(self) -> int:
        """
        Mode indicates the modality (major or minor) of a track, the type of
        scale from which its melodic content is derived. Major is represented
        by 1 and minor is 0.
        """
        return int(self._json_dict['mode'])

    @property
    def popularity(self) -> float:
        """
        The popularity of the track. The value will be between 0 and 100, with
        100 being the most popular. The popularity is calculated by algorithm
        and is based, in the most part, on the total number of plays the track
        has had and how recent those plays are. Note: When applying track
        relinking via the market parameter, it is expected to find relinked
        tracks with popularities that do not match min_*, max_*and target_*
        popularities. These relinked tracks are accurate replacements for
        unplayable tracks with the expected popularity scores. Original, non-
        relinked tracks are available via the linked_from attribute of the
        relinked track response.
        """
        return float(self._json_dict['popularity'])

    @property
    def speechiness(self) -> float:
        """
        Speechiness detects the presence of spoken words in a track. The more
        exclusively speech-like the recording (e.g. talk show, audio book,
        poetry), the closer to 1.0 the attribute value. Values above 0.66
        describe tracks that are probably made entirely of spoken words.
        Values between 0.33 and 0.66 describe tracks that may contain both
        music and speech, either in sections or layered, including such cases
        as rap music. Values below 0.33 most likely represent music and other
        non-speech-like tracks.
        """
        return float(self._json_dict['speechiness'])

    @property
    def tempo(self) -> float:
        """
        The overall estimated tempo of a track in beats per minute (BPM). In
        musical terminology, tempo is the speed or pace of a given piece and
        derives directly from the average beat duration.
        """
        return float(self._json_dict['tempo'])

    @property
    def time_signature(self) -> int:
        """
        An estimated overall time signature of a track. The time signature
        (meter) is a notational convention to specify how many beats are in
        each bar (or measure).
        """
        return int(self._json_dict['time_signature'])

    @property
    def valence(self) -> float:
        """
        A measure from 0.0 to 1.0 describing the musical positiveness conveyed
        by a track. Tracks with high valence sound more positive (e.g. happy,
        cheerful, euphoric), while tracks with low valence sound more negative
        (e.g. sad, depressed, angry).
        """
        return float(self._json_dict['valence'])


class AudioAnalysisObject(SpotifyObject):
    """
    Audio Analysis Object docstring...
    """

    def __repr__(self):
        return f'<AudioAnalysisObject data={self.data}>'

    @property
    def data(self) -> dict:
        """
        The data
        """
        return dict(self._json_dict['data'])


class UserObject(SpotifyObject):
    """
    User Object docstring...
    """

    def __repr__(self):
        return f'<UserObject data={self.data}>'

    @property
    def data(self) -> dict:
        """
        The data
        """
        return dict(self._json_dict['data'])
