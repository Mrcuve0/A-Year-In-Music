from album_class import Album

class Artist(object):
    '''This class defines a 'Artist' object'''
    artistCount = 0
    
    def __init__(self, name, genres=None, albums=None, similarArtists=None):
        self.name = name
        if (genres is None):
            self.genres = []
        else:
            self.genres = genres
        if (albums is None):
            self.albums = []    #[LIST] Albums belonging to this artist
        else:
            self.albums = albums
        if (similarArtists is None):
            self.similarArtists = []
        else:
            sim = []
            for artistSP in similarArtists['artists']:
                sim.append(artistSP['id'])            
            self.similarArtists = sim


    def setName(self, name):
        self.name = name
    
    def setGenre(self, genre):
        self.genre = genre

    def addAlbums(self, album): #Add an album to the list
        self.albums.append(album)

    def getName(self):
        return self.name

    def getGenre(self):
        return self.genre

    def getAlbums(self):
        return self.albums
