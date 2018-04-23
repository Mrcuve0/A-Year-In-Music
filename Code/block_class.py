from artist_class import Artist
from album_class import Album
from song_class import Song



class Block(object):

    def __init__(self, date, moment, artistFromName, albumFromName, songFromName, artistToName, albumToName,
         songToName, isRootNode, isAlbum, isSong, repetitions, device, isStreaming, isFirstTimeListening, notes):
        self.date = date
        self.moment = moment
        self.artistFrom = Artist(artistFromName)
        self.artistTo = Artist(artistToName)
        self.albumFrom = Album(albumFromName)
        self.albumTo = Album(albumToName)
        self.songFrom = Song(songFromName)
        self.songTo = Song(songToName)
        if(isRootNode == 'Y'):
            self.isRootNode = True
        else:
            self.isRootNode = False
        if(isAlbum == 'A'):
            self.isAlbum = True
            self.isSong = False
        elif (isSong == "S"):
            self.isAlbum = False
            self.isSong = True
        if(isStreaming == 'Y'):
            self.isStreaming = True
        else:  
            self.isStreaming = False
        if(isFirstTimeListening == 'Y'):
            self.isFirstTimeListening = True
        else:
            self.isFirstTimeListening = False
        self.notes = notes

    