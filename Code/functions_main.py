
from artist_class import Artist
from album_class import Album
from song_class import Song 

import os
import sys
from io import StringIO
from dotenv import load_dotenv, find_dotenv
import pylast as pl
import discogs_client as dgs_c

dgsE = dgs_c.exceptions

load_dotenv(find_dotenv())

network = pl.LastFMNetwork(api_key=os.getenv('LASTFM_API_KEY'), \
                           api_secret=os.getenv('LASTFM_API_SECRET'), \
                           username=os.getenv('LASTFM_USERNAME'), \
                           password_hash=pl.md5(os.getenv('LASTFM_PASSWD')))

try:
    dgs = dgs_c.Client('AYearInMusic', user_token=os.environ.get('DISCOGS_USER_TOKEN'))
except dgsE.DiscogsAPIError as e:
    print('---Exception raised!---')
    if (e.args[1] == 401 or e.args[1] == 403 or e.args[1] == 501):
        print(e.args[0])

artistConv = {}
albumConv = {}
songConv = {}

artistDgs = None
albumDgs = None
songDgs = None

def stringsComparison(realName, idealName):
    listI = idealName.split()
    listR = realName.split()
    x = 0.0
    if len(listI) != len(listR):
        print("Error, different length!")
    else:
        numSplits = len(listI)
        i = errors = 0
        for el in listR:
            if el != listI[i]:
                errors += 1
            i += 1
        x = float(((numSplits - errors)*100)/numSplits)
    return x

def fileReview(artistName, albumName, songName):
    '''Reviews the input file, looks (on Discogs) for the correct spelling of artistName, albumName and songName.
    In order to avoid too many requests to Discogs server, everytime a name conversion is completed, it's added in a dict, '.*Conv'
    so the next time I'll find the wrong spelling I can look for it in the dict instead of repeating the network request.
    returns: artistName, albumName, songName
    '''
    artistNameOLD = artistName
    albumNameOLD = albumName
    songNameOLD = songName
    
    if (artistNameOLD in artistConv.keys()):    #ArtistName already found and converted
        artistName = artistConv.get(artistNameOLD)
    elif (artistNameOLD in artistConv.values()):
        pass
    else:
        try:
            results = dgs.search(artistName, type='artist')  #release, master, artist, label
            artistDgs = results[0]
            artistName = artistDgs.name
            print(artistName)
            #artistFM = network.get_artist(artistName)
            #artistName = str(artistFM.get_name(properly_capitalized=True))   #Returns the correct name of the artist
        except dgsE.DiscogsAPIError as e:
            print('---Exception raised!---')
            if (e.args[1] == 401 or e.args[1] == 403 or e.args[1] == 501):
                sys.exit(e.args[0])
            else:
                print('Exception error: ' + e.args[1] + ', ' + e.args[0])
                print('\'' + artistNameOLD + '\' not found in Discogs library, mantaining old value...')
                artistName = artistNameOLD
        artistConv[artistNameOLD] = artistName
        
    if (albumNameOLD in albumConv.keys()) :  #AlbumName already found and converted
        albumName = albumConv.get(albumNameOLD) 
    elif (albumNameOLD in albumConv.values()):
        pass
    else:
        try:
            #albumFM = network.get_album(artistName, albumName)
            if (albumName != '//'):
                #albumName = str(albumFM.get_name(properly_capitalized=True)) #Returns the correct name of the album
                results = dgs.search(albumName)
                albumDgs = results[0]
                albumName = str(albumDgs.title).partition(' - ')[2]
                print(albumName) #returns album name
                albumConv[albumNameOLD] = albumName
        except dgsE.DiscogsAPIError as e:
            print('---Exception raised!---')
            if (e.args[1] == 401 or e.args[1] == 403 or e.args[1] == 501):
                sys.exit(e.args[0])
            else:
                print('Exception error: ' + e.args[1] + ', ' + e.args[0])
                print('\'' + albumNameOLD + '\' not found in Discogs library, mantaining old value...')
                albumName = albumNameOLD
                albumConv[albumNameOLD] = albumName
    
    if (songNameOLD in songConv.keys()):    #SongName already found and converted
        songName = songConv.get(songNameOLD)
    elif (songNameOLD in songConv.values()):
        pass
    else:
        try:
            results = dgs.search(albumName)
            albumDgs = results[0]
            realName = songNameOLD.lower()
            j = 0
            tracklistPercentages = []
            maxIndex = -1
            maxX = -1
            for track_el in albumDgs.tracklist:
                tracklistPercentages.append(stringsComparison(realName, str(track_el.title).lower()))
                if tracklistPercentages[j] > maxX:
                    maxX = tracklistPercentages[j]
                    maxIndex = j
                j += 1
            print(tracklistPercentages)
            songName = albumDgs.tracklist[maxIndex].title
            print('A fronte di \'' + songNameOLD + '\' è stato scelto il brano: \'' + songName + '\'')

            songConv[songNameOLD] = songName
        except dgsE.DiscogsAPIError as e:
            print('---Exception raised!---')
            if (e.args[1] == 401 or e.args[1] == 403 or e.args[1] == 501):
                sys.exit(e.args[0])
            else:
                print('Exception error: ' + e.args[1] + ', ' + e.args[0])
                print('\'' + songNameOLD + '\' not found in Discogs library, mantaining old value...')
                songName = songNameOLD
                songConv[songNameOLD] = songName
    
    return (artistName, albumName, songName)

def AASInfoGathering(artistName, albumName, songName, isTo, allArtists, allAlbums, allSongs, device, repetitions, albumOrSong, isFirstTimeListening):
    '''Core function that loads all the data from the CSV file, entering new entries (artist, Album or Song) if none or updating them if already there.
    returns: allArtists, allAlbums, allSongs'''
    
    '''
    artistFM = network.get_artist(artistName)    
    albumFM = network.get_album(artistName, albumName)
    songFM = network.get_track(artistName, songName)
    '''

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
            (album, allSongs) = albumCreation(artistName, albumName, songName, albumDgs, songDgs, allSongs, isTo, device, repetitions, albumOrSong, isFirstTimeListening)
            artist.addAlbums(album) #adding that album on the artist career
            allAlbums[albumName] = album
    else:
        print('Artist \''+ artistName + '\' not found in allArtists')
        print('     Creating an artist object for \'' + artistName + '\'')
            
        #Creating an artist object
        artist = Artist(artistName, artistDgs.get_top_tags(limit=10), None, artistDgs.get_similar(limit=20))
        (album, allSongs) = albumCreation(artistName, albumName, songName, albumDgs, songDgs, allSongs, isTo, device, repetitions, albumOrSong, isFirstTimeListening)

        artist.addAlbums(album) #adding that album on the artist career
            
        print('     Updating \'allArtists\' collection...')
        allArtists[artistName] = artist
        print('     Updating \'allAlbums\' collection...')
        allAlbums[albumName] = album

    return (allArtists, allAlbums, allSongs)

def albumCreation(artistName, albumName, songName, albumDgs, songDgs, allSongs, isTo, device, repetitions, albumOrSong, isFirstTimeListening):
    '''This function creates an album Object, looks (on Discogs) for the tracklist and then updates Song details (duration, date, Number of repetitions etc...)
    returns: album, AllSongs'''

    print('     Creating a tracklist for \'' + albumName + '\'')
    print('     Updating \'allSongs\' collection...')
    trackList = []
    album = Album('//', None, None, None, None, None)
    if (albumName == '//'):

        track = Song(songDgs.get_name(), songDgs.get_duration())
        trackList.append(track)
        album = Album('//', None, None, None, None, None)
        allSongs[songName] = track
    else:
        trackListFM = albumDgs.get_tracks()
        print('         Tracks in this album:\n')
        for track_el in trackListFM:    #creating a tracklist from the info retrieved from lastFM
            track_elName = track_el.get_name()
            track = Song(track_elName, track_el.get_duration())
            trackList.append(track)
            print('             -->' + track_elName)
            allSongs[track_elName] = track
        print('\n')
        print('     Creating album object for \'' + albumName + '\'')
        album = Album(albumName, albumDgs.get_wiki_published_date(), trackList, None, len(trackList), isFirstTimeListening)   #Creating an album object with all the tracks
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