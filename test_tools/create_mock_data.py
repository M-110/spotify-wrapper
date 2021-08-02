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
            print(response)
            print(response.text)
            with open(filename, 'w', encoding='utf8') as file:
                json.dump(response.json(), file)
                print(f'Saved as {filename}')

        return response, error

    return inner


# Monty Python
ALBUM = '4aawyAB9vmqN3uQ7FjRGTy'
ALBUMS = ['382ObEPsp2rxGrnsizN5TX', '1A2GTWGtFfWp7KSQTwWOyo',
          '2noRn2Aes5aoNVsU6iWThc']
ARTIST = '0OdUWJ0sBjDrqHygGUXeCF'
ARTISTS = ['2CIMQHirSU0MQqyYHq0eOx', '57dN52uHvrHOxijzpIgu3E',
           '1vCWHaC5f2uS3yhpwWbIA6']
CATEGORY = 'dinner'
COUNTRY = 'US'
GENRES = ['classical', 'countries']
EPISODE = '512ojhOuo1ktJprKbVcKyQ'
EPISODES = ['77o6BIVlYM3msb4MMIL1jH', '0Q86acNRm6V9GYx55SXKwf']
PLAYLIST = '3cEYpjA9oz9GiPac4AsH4n'
SHOW = '38bS44xjbVVZ3No3ByF1dJ'
SHOWS = ['5CfCWKI5pZ28U0uOzXkDHe', '5as3aKmN2k11yfDDDSrvaZ']
TRACK = '3n3Ppam7vgaVa1iaRUc9Lp'
TRACKS = ['3n3Ppam7vgaVa1iaRUc9Lp', '3twNvmDtFQtAd5gMKedhLD']
QUERY = 'Muse'
QUERY_TYPE = ['track', 'artist']
USER = 'wizzler'
USERS = ['jmperezperez', 'thelinmichael', 'wizzler']


def run_gets_working(sp: SpotifyAPI):
    sp.get_multiple_albums(ALBUMS)
    sp.get_an_album(ALBUM)
    sp.get_an_albums_tracks(ALBUM)

    sp.get_multiple_artists(ARTISTS)
    sp.get_an_artist(ARTIST)
    sp.get_an_artists_top_tracks(ARTIST, COUNTRY)
    sp.get_an_artists_related_artists(ARTIST)
    sp.get_an_artists_albums(ARTIST)

    sp.get_all_new_releases()
    sp.get_all_featured_playlists()
    sp.get_all_categories()

    sp.get_all_new_releases()
    sp.get_all_featured_playlists()
    sp.get_all_categories()

    sp.get_a_category(CATEGORY)
    sp.get_a_categorys_playlists(CATEGORY)

    sp.get_recommendations([ARTIST], GENRES, [TRACK])
    sp.get_recommendation_genres()

    sp.get_multiple_episodes(EPISODES)
    sp.get_an_episode(EPISODE)

    sp.check_if_users_follow_a_playlist(PLAYLIST, USERS)
    sp.get_users_followed_artists('artist')

    sp.get_users_saved_albums()
    sp.check_users_saved_albums(ALBUMS)

    sp.get_users_saved_tracks()
    sp.check_users_saved_tracks(TRACKS)

    sp.get_users_saved_episodes()
    sp.check_users_saved_episodes(EPISODES)

    sp.get_users_saved_shows()
    sp.check_users_saved_shows(SHOWS)

    sp.get_available_markets()

    sp.get_a_users_available_devices()

    sp.get_current_users_recently_played_tracks()

    sp.get_a_list_of_current_users_playlists()
    sp.get_a_list_of_a_users_playlists(USER)

    sp.get_a_playlist(PLAYLIST)
    sp.get_a_playlists_items(PLAYLIST)

    sp.get_a_playlist_cover_image(PLAYLIST)

    sp.get_multiple_shows(SHOWS)
    sp.get_a_show(SHOW)
    sp.get_a_shows_episodes(SHOW)

    sp.get_several_tracks(TRACKS)
    sp.get_a_track(TRACK)

    sp.get_audio_features_for_several_tracks(TRACKS)
    sp.get_audio_features_for_a_track(TRACK)
    sp.get_audio_analysis_for_a_track(TRACK)

    sp.get_current_users_profile()
    sp.get_a_users_profile(USER)


def run_gets(sp: SpotifyAPI):
    """Run through the gets to generate the mock data."""
    # # TODO: type_ should be optional
    # sp.get_following_state_for_artists_or_users('artist', ARTISTS)
    # sp.get_following_state_for_artists_or_users('user', USERS)

    # # TODO: type_ should be optional?
    # sp.get_a_users_top_artists_and_tracks('artists')
    # sp.get_a_users_top_artists_and_tracks('tracks')
    # sp.get_information_about_the_users_current_playback()

    # TODO: Market says optional but shouldn't. Maybe add a parameter to the
    #  yaml to specify which markets are optional.
    # sp.get_the_users_currently_playing_track('us')

    # # sp.create_a_playlist(name='api_test')
    # # sp.reorder_or_replace_a_playlists_items()
    # # sp.remove_items_from_a_playlist()
    # # sp.upload_a_custom_playlist_cover_image()
    # TODO: builder needs to do be fixed for a PagingObject with multiple
    #  returns
    # # sp.search_for_an_item(QUERY, QUERY_TYPE)


if __name__ == '__main__':
    spotify = SpotifyAPI()
    spotify._get = cache_get_locally(spotify._get)
    run_gets(spotify)
