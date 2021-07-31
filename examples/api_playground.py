"""Playground for testing the API"""

from spotifywrapper.api import SpotifyAPI
from spotifywrapper.utilities import cache_get_locally

sp = SpotifyAPI()

sp._get = cache_get_locally(sp._get)

profile = sp.get_multiple_albums(['5fpOhRjx2LEvqLiFBeGlaf','4QIZtPbEAQTu1smtYyDHXz'])
profile2 = sp.get_an_album('4QIZtPbEAQTu1smtYyDHXz')

print(profile)