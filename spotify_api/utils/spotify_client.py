import requests

from whomade.settings import CLIENT_SECRET, CLIENT_ID
from spotify_api.models import SpotifyToken


class SpotifyClient:
    def __init__(self):
        self.base_url = "https://api.spotify.com/v1/"

    def search_albums(self):
        search_input = input("Search for an album: ")
        search_input = search_input.replace(" ", "%20")

        access_token = SpotifyToken.objects.first().token
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        url = f"https://api.spotify.com/v1/search?q=album%3A{search_input}&type=album&limit=50"
        response = requests.get(url, headers=headers)

        return response.json()