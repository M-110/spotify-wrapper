from spotify_wrapper.core import SpotifyAPI
from time import sleep
s = SpotifyAPI()
# a = s.get_an_album('3by7eZIVBbnFQITNv5DYCV')
# a = s.get_multiple_albums(['5Pnctsm9Mi4D6W3DzWckA6', '0SAn8HfltmesCG1k3IJEia', '6qb9MDR0lfsN9a2pw77uJy'])
# a = s.get_multiple_albums([''])
# a = s.get_an_albums_tracks('5Pnctsm9Mi4D6W3DzWckA6')
# a = s.get_multiple_artists(['2fqeW1UtOlUpnobQYoRt5s', '42OhQIA7foe5GX6QoohQHK'])
# a = s.get_an_artist('42OhQIA7foe5GX6QoohQHK')
# a = s.get_an_artists_top_tracks('2fqeW1UtOlUpnobQYoRt5s', 'US')
# a = s.get_an_artists_related_artists('2fqeW1UtOlUpnobQYoRt5s')
# a = s.get_an_artists_albums('2fqeW1UtOlUpnobQYoRt5s', include_groups=['album', 'single'])
# a = s.get_all_new_releases(country='US')
a = s.get_all_featured_playlists()
