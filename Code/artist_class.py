from album_class import Album

class Artist(object):
    '''This class defines a 'Artist' object'''
    artistCount = 0
    
    def __init__(self, name, genre=None, albums=None, similarArtists=None):
        self.name = name
        if (genre is None):
            self.genre = []
        else:
            gen = []
            for rel in iter(genre):
                gen.append(str(rel.item))
            self.genre = gen
        if (albums is None):
            self.albums = []    #[LIST] Albums belonging to this artist
        else:
            self.albums = albums
        if (similarArtists is None):
            self.similarArtists = []
        else:
            sim = []
            for rel in iter(similarArtists):
                sim.append(str(rel.item))
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
