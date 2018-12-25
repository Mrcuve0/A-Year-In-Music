from album_class import Album

class Artist(object):
    '''This class defines a 'Artist' object'''
    artistCount = 0
    
    def __init__(self, name, followers=None, genres=None, albums=None, popularity=None, similarArtists=None):
        self.name = name
        if (followers is None):
            self.followers = -1
        else:
            self.followers = followers
        if (genres is None):
            self.genres = []
        else:
            self.genres = genres
        if (albums is None):
            self.albums = []    #[LIST] Albums belonging to this artist
        else:
            self.albums = albums
        if (popularity is None):
            self.opularity = -1
        else:
            self.popularity = popularity       
        if (similarArtists is None):
            self.similarArtists = []
        else:
            sim = []
            for artistSP in similarArtists['artists']:
                sim.append(artistSP['id'])            
            self.similarArtists = sim

###############################################################

    def setName(self, name):
        self.name = name
    
    def setFollowers(self, followers):
        self.followers = followers
    
    def setGenre(self, genre):
        self.genre = genre

    def setPopularity(self, popularity):
        self.popularity = popularity
        
    def addAlbums(self, album): #Add an album to the list
        self.albums.append(album)

###############################################################

    def getName(self):
        return self.name

    def getFollowers(self, followers):
        return self.followers

    def getGenre(self):
        return self.genre
    
    def getPopularity(self, popularity):
        return self.popularity

    def getAlbums(self):
        return self.albums
