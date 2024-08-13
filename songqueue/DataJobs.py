from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from .models import Artist, Song

class DataJobs:
    def AddArtist(UName, pw):
        A = Artist.objects.create(username = UName, password = pw)
        return A.id

    def UserNameAndPassword(UName, pw):
        A = Artist.objects.filter(username = UName, password = pw)
        if(A):
            return True
        return False   
    
    def GetArtistID(UName, pw):
        A = Artist.objects.get(username = UName, password = pw)
        return A.id
    
    def GetSongs(artistID):
        id1 = 0
        highest = 0
        songs = []
        color = 'w'
        S = Song.objects.filter(artist_id = artistID, played = 0)
        if not S:
            Song.objects.filter(artist_id = artistID).update(played = 0)
        S = Song.objects.filter(artist_id = artistID, played = 0).order_by('?')
        for sCnt, s in enumerate(S):
            if sCnt == 0:
                color = 'g'
                id1 = s.id
            else:
                color = 'w'
            songs.append({"id": s.id, "name": s.name, "color": color})
        S = Song.objects.filter(artist_id = artistID, played__gt = 0).order_by('-played')
        for sCnt, s in enumerate(S):
            if sCnt == 0:
                highest = s.played
            color = 'r'
            songs.append({"id": s.id, "name": s.name, "color": color})
        Song.objects.filter(id = id1).update(played = highest + 1)
        return songs
    
    def UndoPlayed(artistID):
      #  arg = args.order_by('-rating').first()
        S = Song.objects.filter(artist_id = artistID).order_by('-played').first()
        if S:
            id = S.id
            Song.objects.filter(id = id).update(played = 0)
      #  for sCnt, s in enumerate(S):
          #  if sCnt == 0:
            #    s.update(played = 100)
             #   break
    
    def AddSongs(artistID, songs):
        for s in songs:
          Song.objects.create(artist_id = artistID, played = 0, name = s)
          
    def DeleteSong(artistID, songID):
        Song.objects.filter(artist_id = artistID, id = songID).delete()