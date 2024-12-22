from django.db import models

# Create your models here.
class SpotifyToken(models.Model):
    token = models.CharField(max_length=512)
    expires_at = models.DateTimeField(auto_now_add=True)




class Artist(models.Model):
    artist_id = models.CharField(max_length=512)
    artist_name = models.CharField(max_length=512)
    artist_url = models.CharField(max_length=512)

class Album(models.Model):
    album_id = models.CharField(max_length=512)
    album_name = models.CharField(max_length=512)
    album_image = models.CharField(max_length=512)
    album_url = models.CharField(max_length=512)
    album_release_date = models.CharField(max_length=512)
    album_type = models.CharField(max_length=512)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
