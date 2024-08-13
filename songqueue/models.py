from django.db import models

class Artist(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    
class Song(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    played = models.IntegerField(default=0)