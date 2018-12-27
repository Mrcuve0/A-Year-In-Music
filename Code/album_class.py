from song_class import Song

class Album(object):
    '''This class defines a 'Album' object'''
    albumCount = 0

    def __init__(self, ID, name, releaseDate=None, releaseDatePrecision=None, label=None, popularity=None, tracks=None, duration=None, numTracks=None, isFirstTimeListening=None):
        self.ID = ID
        self.name = name
        if (releaseDate is None):
            self.releaseDate = -1
        else:
            self.releaseDate = releaseDate
        if (releaseDatePrecision is None):
            self.releaseDatePrecision = ""
        else:
            self.releaseDatePrecision = releaseDatePrecision
        if (label is None):
            self.label = ""
        else:
            self.label = label
        if (popularity is None):
            self.popularity = -1
        else:
            self.popularity = popularity
        if (tracks is None):
            self.tracks = []
        else:
            self.tracks = tracks #[LIST] Tracks belonging to this album
        if (duration is None):
            self.duration = 0
        else:
            self.duration = duration
        if (numTracks is None):
            self.numTracks = -1
        else:
            self.numTracks = numTracks
        if (isFirstTimeListening is None):
            self.isFirstTimeListening = None
        else: 
            self.isFirstTimeListening = isFirstTimeListening
        #self.composer = ""

###############################################################

    def __str__(self):
        return self.name

    def setID(self, ID):
        '''sets the ID of this album'''
        self.ID = ID

    def setName(self, name):
        '''sets the name of this album'''
        self.name = name
    
    def setReleaseDate(self, releaseDate):
        '''sets the releaseDate of this album'''
        self.releaseDate = releaseDate

    def setReleaseDatePrecision(self, releaseDatePrecision):
        '''sets the releaseDatePrecision of this album'''
        self.releaseDatePrecision = releaseDatePrecision

    def setLabel(self, label):
        '''sets the label of this album'''
        self.label = label

    def setPopularity(self, popularity):
        '''sets the popularity of this album'''
        self.popularity = popularity

    def addTracks(self, song):
        '''adds a track to the tracklist of the album'''
        self.tracks.append(song)

    def setDuration(self):
        '''set the total duration of this album, based on the sum of tracks durations'''
        tot = 0
        for track in self.tracks:
            tot += int(track.getDuration())
        self.duration = tot

    def setNumTracks(self, numTracks):
        '''the muber of tracks available in the tracklist of the album'''
        self.numTracks = numTracks

    def setIsFirstTimeListening(self, isFirstTimeListening):
        '''sets if isFirsttimeListeninf of this album'''
        self.isFirstTimeListening = isFirstTimeListening

    def updateRepetitions(self, device, repetitions):
        trackList = self.getTracks()
        for track in trackList:
            track.updateRepetitions(device, repetitions)

###############################################################
    
    def getID(self):
        '''returns the ID of this album'''
        return self.ID

    def getName(self):
        '''returns the name of this album'''
        return self.name

    def getReleaseDate(self):
        '''returns the releaseDate of this album'''
        return self.releaseDate

    def getReleaseDatePrecision(self):
        '''returns the releaseDatePrecision of this album'''
        return self.releaseDatePrecision

    def getLabel(self, label):
        '''returns the label of this album'''
        return self.label
    
    def getPopularity(self, popularity):
        '''returns the popularity of this album'''
        return self.popularity

    def getTracks(self):
        '''returns a list of all tracks belonging to this album'''
        return self.tracks

    def getDuration(self):
        '''returns the total duration of this album'''
        return self.duration

    def getNumTracks(self):
        '''returns the number of tracks belonging to this album'''
        return self.numTracks

    def getIsFirstTimeListening(self):
        '''returns isFirstTimeListening parameter this album'''
        return self.isFirstTimeListening