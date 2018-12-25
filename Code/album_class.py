from song_class import Song

class Album(object):
    '''This class defines a 'Album' object'''
    albumCount = 0

    def __init__(self, name, releaseDate=None, tracks=None, duration=None, num_tracks=None, isFirstTimeListening=None):
        self.name = name
        if (releaseDate is None):
            self.releaseDate = 0
        else:
            self.releaseDate = releaseDate
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

###############################################################

    def __str__(self):
        return self.name

    def setName(self, name):
        '''sets the name of this album'''
        self.name = name
    
    def setYear(self, releaseDate):
        '''sets the releaseDate of this album'''
        self.releaseDate = releaseDate

    def setDuration(self):
        '''set the total duration of this album, based on the sum of tracks durations'''
        tot = 0
        for track in self.tracks:
            tot += int(track.getDuration())
        self.duration = tot

    def addTracks(self, song):
        '''adds a track to the tracklist of the album'''
        self.tracks.append(song)

###############################################################
    

    def getName(self):
        '''returns the name of this album'''
        return self.name

    def getReleaseDate(self):
        '''returns the releaseDate of this album'''
        return self.releaseDate

    def getDuration(self):
        '''returns the total duration of this album'''
        return self.duration

    def getTracks(self):
        '''returns a list of all tracks belonging to this album'''
        return self.tracks

    def getNum_tracks(self):
        '''returns the number of tracks belonging to this album'''
        return len(self.tracks)

    def updateRepetitions(self, device, repetitions):
        trackList = self.getTracks()
        for track in trackList:
            track.updateRepetitions(device, repetitions)