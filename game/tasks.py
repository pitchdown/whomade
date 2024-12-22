from celery import shared_task
import random
from spotify_api.models import Album, Artist
import requests
from PIL import Image, ImageFilter
from io import BytesIO
import base64

@shared_task
def fetch_album_data():
    album_ids = list(Album.objects.values_list('id', flat=True))
    random.shuffle(album_ids)
    unique_album_ids = album_ids[:10]

    albums = Album.objects.filter(id__in=unique_album_ids)
    game_data = []

    for album in albums:
        incorrect_artists = (
            Artist.objects.exclude(id=album.artist.id)
            .order_by('?')
            .values_list('artist_name', flat=True)[:3]
        )
        incorrect_artists = [artist.upper() for artist in incorrect_artists]

        correct_artist = album.artist.artist_name.upper()
        all_artists = incorrect_artists + [correct_artist]
        random.shuffle(all_artists)

        url = album.album_image
        response = requests.get(url)
        if response.status_code == 200:
            image = Image.open(BytesIO(response.content))
            blur_radius = 10
            blurred_image = image.filter(ImageFilter.GaussianBlur(blur_radius))

            img_io = BytesIO()
            blurred_image.save(img_io, format='JPEG')
            img_io.seek(0)
            base64_image = base64.b64encode(img_io.getvalue()).decode()
            img_data = f"data:image/jpeg;base64,{base64_image}"

            game_data.append({
                'album_name': album.album_name.upper(),
                'album_image': img_data,
                'artists': all_artists,
                'correct_artist': correct_artist
            })

    return game_data
