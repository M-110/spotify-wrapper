"""Playground for testing the API"""

from spotifywrapper.api import SpotifyAPI

sp = SpotifyAPI()

profile = sp.get_multiple_albums(['5fpOhRjx2LEvqLiFBeGlaf','4QIZtPbEAQTu1smtYyDHXz'])

print(profile)