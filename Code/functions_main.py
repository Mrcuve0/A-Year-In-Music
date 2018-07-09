
from artist_class import Artist
from album_class import Album
from song_class import Song 
import pylast as pl

api_file = open('config.ini', 'r')
APIS = api_file.read().split('\n')
api_file.close()
API_KEY = APIS[0]
API_SECRET = APIS[1]
USERNAME = APIS[2]
PASSWORD_HASH = pl.md5(APIS[3])

network = pl.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET, username=USERNAME, password_hash=PASSWORD_HASH)

artistConv = {}
albumConv = {}
songConv = {}


def albumCreation(artistName, albumName, songName, albumFM, songFM, allSongs, isTo, device, repetitions, albumOrSong, isFirstTimeListening):
    '''This function creates an album Object'''
    print('     Creating a tracklist for \'' + albumName + '\'')
    print('     Updating \'allSongs\' collection...')
    trackList = []
    album = Album('//', None, None, None, None, None)
    if (albumName == '//'):
        track = Song(songFM.get_name(), songFM.get_duration())
        trackList.append(track)
        album = Album('//', None, None, None, None, None)
        allSongs[songName] = track
    else:
        trackListFM = albumFM.get_tracks()
        print('         Tracks in this album:\n')
        for track_el in trackListFM:    #creating a tracklist from the info retrieved from lastFM
            track_elName = track_el.get_name()
            track = Song(track_elName, track_el.get_duration())
            trackList.append(track)
            print('             -->' + track_elName)
            allSongs[track_elName] = track
        print('\n')
        print('     Creating album object for \'' + albumName + '\'')
        album = Album(albumName, albumFM.get_wiki_published_date(), trackList, None, len(trackList), isFirstTimeListening)   #Creating an album object with all the tracks
        album.setDuration() #calculating the total duration of the album
    
    if (isTo == True and albumOrSong == 'S'):
        song = allSongs[songName]
        song.updateRepetitions(device, repetitions)
    else:
        print('         I\'m not updating \'PlayCount\' for this specific song: isTo = ' + str(isTo) + ', albumOrSong = ' + str(albumOrSong))

    if (isTo == True and albumOrSong == 'A'):
        album.updateRepetitions(device, repetitions)
    else:
        print('         I\'m not updating \'PlayCount\' for this specific album: isTo = ' + str(isTo) + ', albumOrSong = ' + str(albumOrSong))

    return (album, allSongs)
        
def AASInfoGathering(artistName, albumName, songName, isTo, allArtists, allAlbums, allSongs, device, repetitions, albumOrSong, isFirstTimeListening):
    '''This function loads all the data from the CSV file, entering new entries if none or updating them if already there'''
    
    artistFM = network.get_artist(artistName)    
    albumFM = network.get_album(artistName, albumName)
    songFM = network.get_track(artistName, songName)

    if (artistName in str(allArtists.keys())):
        print('     Artist \'' + artistName + '\' already added!')
        print('     Gathering Album \'' + albumName + '\' info...')
        if (albumName in str(allAlbums.keys())):
            print('     Album \'' + albumName + '\' already added!')
            print('     Gathering Song \'' + songName + '\' info...')
            if (songName in str(allSongs.keys())):
                print('     Song \'' + songName + '\' already added!')
                print('     Updating Song \'' + songName + '\' info...')
                if (isTo == True and albumOrSong == 'S'):
                    song = allSongs[songName]
                    song.updateRepetitions(device, repetitions)
                else:
                    print('         I\'m not updating \'PlayCount\' for this specific song: isTo = ' + str(isTo) + ', albumOrSong = ' + str(albumOrSong))
            else:
                print('         FATAL ERROR, SONG \'' + songName + '\' NOT FOUND!') #All the songs should already be in their respective albums
                pass
            if (isTo == True and albumOrSong == 'A'):
                album = allAlbums[albumName]
                album.updateRepetitions(device, repetitions)
            else:
                print('         I\'m not updating \'PlayCount\' for this specific album: isTo = ' + str(isTo) + ', albumOrSong = ' + str(albumOrSong))
        else:   #Album not found
            print('         Album \'' + albumName + '\' not found, collecting info and adding it...')
            artist = allArtists[artistName]
            (album, allSongs) = albumCreation(artistName, albumName, songName, albumFM, songFM, allSongs, isTo, device, repetitions, albumOrSong, isFirstTimeListening)
            artist.addAlbums(album) #adding that album on the artist career
            allAlbums[albumName] = album
    else:
        print('Artist \''+ artistName + '\' not found in allArtists')
        print('     Creating an artist object for \'' + artistName + '\'')
            
        #Creating an artist object
        artist = Artist(artistName, artistFM.get_top_tags(limit=10), None, artistFM.get_similar(limit=20))
        (album, allSongs) = albumCreation(artistName, albumName, songName, albumFM, songFM, allSongs, isTo, device, repetitions, albumOrSong, isFirstTimeListening)

        artist.addAlbums(album) #adding that album on the artist career
            
        print('     Updating \'allArtists\' collection...')
        allArtists[artistName] = artist
        print('     Updating \'allAlbums\' collection...')
        allAlbums[albumName] = album

    return (allArtists, allAlbums, allSongs)

def fileReview(artistName, albumName, songName):
    artistNameOLD = artistName
    albumNameOLD = albumName
    songNameOLD = songName
    
    if (artistNameOLD in artistConv.keys()):    #Artist already found and converted
        artistName = artistConv.get(artistNameOLD)
    elif (artistNameOLD in artistConv.values()):
        pass
    else:
        try:
            artistFM = network.get_artist(artistName)
            artistName = str(artistFM.get_name(properly_capitalized=True))   #Returns the correct name of the artist
            artistConv[artistNameOLD] = artistName
        except pl.WSError as e:
            #print(str(e.get_id()))
            print('---Exception raised!---')
            if str(e.get_id()) == str(6):
                print('\'' + artistNameOLD + '\' not found in LastFM library, mantaining old value...')
                artistName = artistNameOLD
                artistConv[artistNameOLD] = artistName
        
    if (albumNameOLD in albumConv.keys()) :  #Album already found and converted
        albumName = albumConv.get(albumNameOLD) 
    elif (albumNameOLD in albumConv.values()):
        pass
    else:
        try:
            albumFM = network.get_album(artistName, albumName)
            if (albumName != '//'):
                albumName = str(albumFM.get_name(properly_capitalized=True)) #Returns the correct name of the album
                albumConv[albumNameOLD] = albumName
        except pl.WSError as e:
            #print(str(e.get_id()))
            print('---Exception raised!---')
            if str(e.get_id()) == str(6):
                print('\'' + albumNameOLD + '\' not found in LastFM library, mantaining old value...')
                albumName = albumNameOLD
                albumConv[albumNameOLD] = albumName
    
    if (songNameOLD in songConv.keys()):    #Song already found and converted
        songName = songConv.get(songNameOLD)
    elif (songNameOLD in songConv.values()):
        pass
    else:
        try:
            songFM = network.get_track(artistName, songName)
            songName = str(songFM.get_title(properly_capitalized=True))   #Returns the correct name of the song
            songConv[songNameOLD] = songName
        except pl.WSError as e:
            #print(str(e.get_id()))
            print('---Exception raised!---')
            if str(e.get_id()) == str(6):
                print('\'' + songNameOLD + '\' not found in LastFM library, mantaining old value...')
                songName = songNameOLD
                songConv[songNameOLD] = songName
    
    return (artistName, albumName, songName)