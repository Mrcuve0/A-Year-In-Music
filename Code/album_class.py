from song_class import Song

class Album(object):
    '''This class defines a 'Album' object'''
    albumCount = 0

    def __init__(self, name, year=None, tracks=None, duration=None, num_tracks=None, isFirstTimeListening=None):
        self.name = name
        if (year is None):
            self.year = 0
        else:
            self.year = year
        if (tracks is None):
            self.tracks = []
        else:
            self.tracks = tracks #[LIST] Tracks belonging to this album
        if (duration is None):
            self.duration = 0
        else:
            self.duration = duration
        if (isFirstTimeListening is None):
            self.isFirstTimeListening = None
        else: 
            self.isFirstTimeListening = isFirstTimeListening
        #self.composer = ""

    def __str__(self):
        return self.name

    def setName(self, name):
        '''sets the name of this album'''
        self.name = name
    
    def setYear(self, year):
        '''sets the year of release of this album'''
        self.year = year

    def addTracks(self, song):
        '''adds a track to the tracklist of the album'''
        self.tracks.append(song)

    def setDuration(self):
        '''set the total duration of this album, based on the sum of tracks durations'''
        tot = 0
        for track in self.tracks:
            tot += int(track.getDuration())
        self.duration = tot

    '''
    def setComposer(self, composer):
        self.composer = composer
    '''

    '''
    def setArtist(self, artist):
        self.artist = artist
    '''

    def getName(self):
        '''returns the name of this album'''
        return self.name

    def getYear(self):
        '''returns the year of releas of this album'''
        return self.year

    def getDuration(self):
        '''returns the total duration of this album'''
        return self.duration

    '''
    def getComposer(self):
        return self.composer
    '''

    def getTracks(self):
        '''returns a list of all tracks belonging to this album'''
        return self.tracks

    def getNum_tracks(self):
        '''returns the number of tracks belonging to this album'''
        return len(self.tracks)

    '''def getArtist(self):
        return self.artist'''