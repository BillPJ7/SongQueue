from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from .DataJobs import DataJobs
import json

def index(request):
    if request.method == "POST":
        userName = request.POST['UName']
        password = request.POST['Pwd']
        newUser = 'btnNewUser' in request.POST
        existingUser = 'btnExistingUser' in request.POST
        existingCred = DataJobs.UserNameAndPassword(userName, password)
        if (newUser and not existingCred) or (existingUser and existingCred):
            songs = []
            if newUser:
                artistID = DataJobs.AddArtist(userName, password)
            else: 
                artistID = DataJobs.GetArtistID(userName, password)
                songs = DataJobs.GetSongs(artistID)
            songs = json.dumps(songs)
            context = {"songs": songs, "artistid": artistID}
            return render(request, 'songqueue/songs.html', context)
        if (existingUser and not existingCred):
            context = {"msg": 'change'}
        else:
            context = {"msg": 'nochange'}  
        return render(request, 'songqueue/index.html', context)
    context = {"msg": 'nochange'}
    return render(request, 'songqueue/index.html', context)

def songs(request):
    if request.method == "POST":
        artistID = request.POST['ArtistID']
        submitFunction = request.POST['SubmitFunction']
        if submitFunction == 'Change':
            context = {"msg": 'change'}
            return render(request, 'songqueue/index.html', context)
        if submitFunction == 'Add':
            context = {"artistid": artistID}
            return render(request, 'songqueue/addsongs.html', context)
        if submitFunction == 'Delete':
            songID = request.POST['Delete']
            DataJobs.DeleteSong(artistID, songID)
        songs = json.dumps(DataJobs.GetSongs(artistID))
        if submitFunction == 'Delete':
            DataJobs.UndoPlayed(artistID)
        context = {"songs": songs, "artistid": artistID, "msg": 'nochange'}   
        return render(request, 'songqueue/songs.html', context)
    return render(request, 'songqueue/songs.html')

def addsongs(request):
    if request.method == "POST":
        artistID = request.POST['ArtistID']
       # print('artistID')
       # print(artistID)
        DataJobs.AddSongs(artistID, json.loads(request.POST['ReturnInfo']))
        songs = DataJobs.GetSongs(artistID)
        DataJobs.UndoPlayed(artistID)
        songs = json.dumps(songs)
        context = {"songs": songs, "artistid": artistID, "msg": 'nochange'}
        return render(request, 'songqueue/songs.html', context, False)
    return render(request, 'songqueue/addsongs.html')