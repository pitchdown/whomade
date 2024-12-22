from django.core.management.base import BaseCommand, CommandError
from whomade.settings import CLIENT_ID, CLIENT_SECRET
from spotify_api.utils.spotify_client import SpotifyClient
from spotify_api.models import Album, Artist


class Command(BaseCommand):
    help = 'Fetches artist data from Spotify API'

    def handle(self, *args, **options):
        response = SpotifyClient.search_albums(self)
        albums = response['albums']['items']
        for album in albums:
            album_data = {
                'album_id': album['id'],
                'album_name': album['name'],
                'album_image': album['images'][0]['url'],
                'album_url': album['external_urls']['spotify'],
                'album_release_date': album['release_date'],
                'album_type': album['album_type']
            }

            artist_data = {
                'artist_id': album['artists'][0]['id'],
                'artist_name': album['artists'][0]['name'],
                'artist_url': album['artists'][0]['external_urls']['spotify']
            }

            if not Artist.objects.filter(artist_id=artist_data['artist_id']).exists():
                Artist.objects.create(**artist_data)
            artist = Artist.objects.get(artist_id=artist_data['artist_id'])

            if not Album.objects.filter(album_id=album_data['album_id']).exists():
                Album.objects.create(**album_data, artist=artist)

