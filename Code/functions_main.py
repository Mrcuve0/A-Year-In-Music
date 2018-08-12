
from artist_class import Artist
from album_class import Album
from song_class import Song 

import os
import sys
from dotenv import load_dotenv, find_dotenv
import pylast as pl
import discogs_client as dgs_c
import spotipy
from fuzzywuzzy import process
from spotipy.oauth2 import SpotifyClientCredentials

load_dotenv(find_dotenv())

######## LAST FM ########
network = pl.LastFMNetwork(api_key=os.getenv('LASTFM_API_KEY'), \
                           api_secret=os.getenv('LASTFM_API_SECRET'), \
                           username=os.getenv('LASTFM_USERNAME'), \
                           password_hash=pl.md5(os.getenv('LASTFM_PASSWD')))

######## DISCOGS ########
dgsE = dgs_c.exceptions
try:
    dgs = dgs_c.Client('AYearInMusic', user_token=os.environ.get('DISCOGS_USER_TOKEN'))
except dgsE.DiscogsAPIError as e:
    print('---Exception raised!---')
    if (e.args[1] == 401 or e.args[1] == 403 or e.args[1] == 501):
        print(e.args[0])

######## SPOTIFY ########
client_credentials_mng = SpotifyClientCredentials(os.getenv('SPOTIFY_CLIENT_ID'), os.getenv('SPOTIFY_CLIENT_SECRET'))
sp = spotipy.Spotify(client_credentials_manager=client_credentials_mng)

spE = spotipy.SpotifyException

artistConv = {}
albumConv = {}
songConv = {}

artistTR = {}
albumTR = {}
songTR  = {}

artistTR_opposite = {}
albumTR_opposite = {}
songTR_opposite = {}

artistSP = None
albumSP = None
songSP = None

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

def fileReview(artistName, albumName, songName, artistID, albumID, songID):
    '''Reviews the input file, looks (on Spotify) for the correct spelling of artistName, albumName and songName.
    In order to avoid too many requests to Spotify server, everytime a name conversion is completed, it's added in a dict, '.*Conv'
    so the next time I'll find the wrong spelling I can look for it in the dict instead of repeating the network request.
    returns: artistName, albumName, songName
    '''
    artistNameOLD = artistName
    albumNameOLD = albumName
    songNameOLD = songName
    
    if (artistNameOLD in artistConv.keys()):    #ArtistName already found and converted
        artistName = artistConv.get(artistNameOLD)
        artistID = artistTR_opposite.get(artistName)

    elif (artistNameOLD in artistConv.values()):
        pass
    else:
        try:
            if (str(artistName).lower() == str('Butch').lower()):
                artistID = str('5kLzaeSHrmS7okc5XNE6lv')
            else:
                artistSP = sp.search(q='artist:\"' + artistName + '\"', type='artist')

                artists_list = []
                if artistSP['artists']['total'] > artistSP['artists']['limit']:
                    max_range = 'limit'
                else:
                    max_range = 'total'
                for i in range(0, artistSP['artists'][max_range]):
                    artists_list.append(artistSP['artists']['items'][i]['name'])

                result = process.extractOne(artistName, artists_list)
                index = artists_list.index(result[0])
                artistName = artistSP['artists']['items'][index]['name']
                artistID = artistSP['artists']['items'][index]['id'] 
        except TypeError:
            print('\'' + artistName + '\' Not Found! Keeping old value... TypeError')
        except IndexError:
            print('\'' + artistName + '\' Not Found! Keeping old value... IndexError') 
        except spE as e: 
            print('---Exception raised!---')
            if (str(e.http_status) == str(401)):    #Unauthorized
                print('The request requires user authentication or, if the request included authorization credentials, authorization has been refused for those credentials.')
                sys.exit(e.msg)
            if (str(e.http_status) == str(204)):    #No Content
                print('The request has succeeded but returns no message body.')
                sys.exit(e.msg)
            elif (str(e.http_status) == str(404)):    #Not Found
                print('The requested resource could not be found. This error can be due to a temporary or permanent condition.')
                sys.exit(e.msg)
            elif (str(e.http_status) == str(502)):    #Bad Gateway
                print('The server was acting as a gateway or proxy and received an invalid response from the upstream server.')
                sys.exit(e.msg)
            else:
                print('Exception error: ' + str(e.http_status) + ', ' + str(e.msg))
            print('\'' + artistNameOLD + '\' not found in Spotify library, mantaining old value...')
            artistName = artistNameOLD
        artistConv[artistNameOLD] = artistName
        artistTR[artistID] = artistName
        artistTR_opposite[artistName] = artistID

    print('artistName: ' + artistName + ', ID: ' + artistID)
        
    if (albumNameOLD in albumConv.keys()) :  #AlbumName already found and converted
        albumName = albumConv.get(albumNameOLD) 
        albumID = albumTR_opposite.get(albumName)
    elif (albumNameOLD in albumConv.values()):
        pass
    else:
        try:
            if (str(albumName).lower() == str('Rage Against The Machine').lower()):
                albumID = str('4LaRYkT4oy47wEuQgkLBul')
            elif (str(albumName).lower() == str('Dope').lower()):
                albumID = '7zPgCo3kXvezF86DQw2ERZ' 
            elif (str(albumName).lower() == str('Dream Sequence').lower()):
                albumID = '7ALFR4o9ZXfqNVv9EOORn1'
            elif (str(albumName).lower() == str('My Salsoul').lower()):
                albumID = str('My Salsoul')
            elif (str(albumName).lower() == str('Sacrebleu').lower()):
                albumID = str('Sacrebleu')
            elif (str(albumName).lower() == str('Until One').lower()):
                albumID = str('5JRoPXvkRBmwyAA2fkMWgY')

            else:
                albumSP = sp.search(q=str('\"' + artistName + '\" \"' + albumName + '\" NOT ' + 'Anniversary'), type='album')
                if (albumName != '//' and albumSP['albums']['total'] != 0):     
                    albums_list = []

                    if albumSP['albums']['total'] > albumSP['albums']['limit']:
                        max_range = 'limit'
                    else:
                        max_range = 'total'
                    for i in range(0, albumSP['albums'][max_range]):
                        albums_list.append(albumSP['albums']['items'][i]['name'])
                    result = process.extractOne(albumName, albums_list)
                    index = albums_list.index(result[0])
                    albumName = albumSP['albums']['items'][index]['name']
                    albumID = albumSP['albums']['items'][index]['id']          
                    
                    #albumConv[albumNameOLD] = albumName
                elif (albumSP['albums']['total'] == 0):
                    print('\'' + albumName + '\' Not Found! Keeping old value...')
                    albumID = None
        except TypeError:
            print('\'' + albumName + '\' Not Found! Keeping old value...')        
        except IndexError:
            print('\'' + albumName + '\' Not Found! Keeping old value...')  
        except spE as e: 
            print('---Exception raised!---')
            if (str(e.http_status) == str(401)):    #Unauthorized
                print('The request requires user authentication or, if the request included authorization credentials, authorization has been refused for those credentials.')
                sys.exit(e.msg)
            if (str(e.http_status) == str(204)):    #No Content
                print('The request has succeeded but returns no message body.')
                sys.exit(e.msg)
            elif (str(e.http_status) == str(404)):    #Not Found
                print('The requested resource could not be found. This error can be due to a temporary or permanent condition.')
                sys.exit(e.msg)
            elif (str(e.http_status) == str(502)):    #Bad Gateway
                print('The server was acting as a gateway or proxy and received an invalid response from the upstream server.')
                sys.exit(e.msg)
            else:
                print('Exception error: ' + str(e.http_status) + ', ' + str(e.msg))
            albumName = albumNameOLD
        albumConv[albumNameOLD] = albumName
        albumTR[albumID] = albumName
        albumTR_opposite[albumName] = albumID

    print('albumName: ' + albumName + ', ID: ' + albumID)
    
    if (songNameOLD in songConv.keys()):    #SongName already found and converted
        songName = songConv.get(songNameOLD)
        songID = songTR_opposite.get(songName)
    elif (songNameOLD in songConv.values()):
        pass
    else:
        try:
            if (str(songName).lower() == str('Killing in the Name').lower()):
                songID = str('3FUS56gKr9mVBmzvlnodlh')
            elif (str(songName).lower() == str('Dope - Original Mix').lower()):
                songID = str('5wElWRFQIzeE1YBe1gTIxp')
            elif (str(songName).lower() == str('The Dream Is Always The Same').lower()):
                songID = str('5iRVl2TQ54sk9KMed2iUDy')
            elif (str(songName).lower() == str('Seconds').lower()):
                songID = str('Seconds')
            elif (str(songName).lower() == str('Prologue').lower()):
                songID = str('Prologue')
            elif (str(songName).lower() == str('Leave the World Behind').lower()):
                songID = str('3ueNIaHaq1EvW6OOzfGXz7')
            else:
                trackSP = sp.search(q=str('artist:' + artistName + ' album:' + albumName + ' track:' + songName), type='track')

                songs_list = []
                if trackSP['tracks']['total'] > trackSP['tracks']['limit']:
                    max_range = 'limit'
                else:
                    max_range = 'total'
                for i in range(0, trackSP['tracks'][max_range]):
                    songs_list.append(trackSP['tracks']['items'][i]['name'])
                result = process.extractOne(songName, songs_list)
                index = songs_list.index(result[0])
                songName = trackSP['tracks']['items'][index]['name']
                songID = trackSP['tracks']['items'][index]['id']

        except TypeError:
            print('\'' + songName + '\' Not Found! Keeping old value...')
        except IndexError:
            print('\'' + songName + '\' Not Found! Keeping old value...')  
        except spE as e: 
            print('---Exception raised!---')
            if (str(e.http_status) == str(401)):    #Unauthorized
                print('The request requires user authentication or, if the request included authorization credentials, authorization has been refused for those credentials.')
                sys.exit(e.msg)
            if (str(e.http_status) == str(204)):    #No Content
                print('The request has succeeded but returns no message body.')
                sys.exit(e.msg)
            elif (str(e.http_status) == str(404)):    #Not Found
                print('The requested resource could not be found. This error can be due to a temporary or permanent condition.')
                sys.exit(e.msg)
            elif (str(e.http_status) == str(502)):    #Bad Gateway
                print('The server was acting as a gateway or proxy and received an invalid response from the upstream server.')
                sys.exit(e.msg)
            else:
                print('Exception error: ' + str(e.http_status) + ', ' + str(e.msg))
            print('\'' + songNameOLD + '\' not found in Discogs library, mantaining old value...')
            songName = songNameOLD
        songConv[songNameOLD] = songName
        songTR[songID] = songName
        songTR_opposite[songName] = songID

    print('songName: ' + songName + ', ID: ' + songID)
    return (artistID, albumID, songID)

def AASInfoGathering(artistID, albumID, songID, isTo, allArtists, allAlbums, allSongs, device, repetitions, albumOrSong, isFirstTimeListening):
    '''Core function that loads all the data from the CSV file, entering new entries (artist, Album or Song) if none or updating them if already there.
    returns: allArtists, allAlbums, allSongs'''
    
    '''
    artistFM = network.get_artist(artistName)    
    albumFM = network.get_album(artistName, albumName)
    songFM = network.get_track(artistName, songName)
    '''

    if (artistID == '5Il27M5JXuQLgwDgVrQMgo'):   #Dimitri from Paris
        return

    if (artistID in allArtists.keys()):
        print('     Artist \'' + str(artistTR[artistID]) + '\' already added!')
        print('     Gathering Album \'' + str(albumTR[albumID]) + '\' info...')
        if (albumID in allAlbums.keys()):
            print('     Album \'' + str(albumTR[albumID]) + '\' already added!')
            print('     Gathering Song \'' + str(songTR[songID]) + '\' info...')
            if (songID in allSongs.keys()):
                print('     Song \'' + str(songTR[songID]) + '\' already added!')
                print('     Updating Song \'' + str(songTR[songID]) + '\' info...')
                if (isTo == True and albumOrSong == 'S'):
                    song = allSongs[songID]
                    song.updateRepetitions(device, repetitions)
                else:
                    print('         Im not updating \'PlayCount\' for this specific song: isTo = ' + str(isTo) + ', albumOrSong = ' + str(albumOrSong))
            else:
                print('         FATAL ERROR, SONG \'' + songTR[songID] + '\' NOT FOUND!') #All the songs should already be in their respective albums
                pass
            if (isTo == True and albumOrSong == 'A' and (albumID != 'My Salsoul' or albumID != 'Sacrebleu')):
                album = allAlbums[albumID]
                album.updateRepetitions(device, repetitions)
            else:
                print('         Im not updating \'PlayCount\' for this specific album: isTo = ' + str(isTo) + ', albumOrSong = ' + str(albumOrSong))
        else:   #Album not found
            print('         Album \'' + albumTR[albumID] + '\' not found, collecting info and adding it...')
            artist = allArtists[artistID]
            (album, allSongs) = albumCreation(artistID, albumID, songID, songSP, allAlbums, allSongs, isTo, device, repetitions, albumOrSong, isFirstTimeListening)
            artist.addAlbums(album) #adding that album on the artist career
            allAlbums[albumID] = album
    else:
        print('Artist \''+ str(artistTR[artistID]) + '\' not found in allArtists')
        print('     Creating an artist object for \'' + str(artistTR[artistID]) + '\'')
            
        #Creating an artist object
        artistSP = sp.artist(artistID)
        artistName = artistSP['name']
        artist = Artist(artistName, artistSP['genres'], None, sp.artist_related_artists(artistID))
        if (albumID == str('My Salsoul')  or albumID == str('Sacrebleu')):
            album = None
        else:     
            (album, allSongs) = albumCreation(artistID, albumID, songID, songSP, allAlbums, allSongs, isTo, device, repetitions, albumOrSong, isFirstTimeListening)
            artist.addAlbums(album) #adding that album on the artist career 
        print('     Updating \'allArtists\' collection...')
        allArtists[artistID] = artist    
        print('     Updating \'allAlbums\' collection...')
        allAlbums[albumID] = album
    return (allArtists, allAlbums, allSongs)

def albumCreation(artistID, albumID, songID, songSP, allAlbums, allSongs, isTo, device, repetitions, albumOrSong, isFirstTimeListening):
    '''This function creates an album Object, looks (on Discogs) for the tracklist and then updates Song details (duration, date, Number of repetitions etc...)
    returns: album, AllSongs'''

    print('     Creating a tracklist for \'' + str(albumTR[albumID]) + '\'')
    print('     Updating \'allSongs\' collection...')
    trackList = []
    album = Album(None, None, None, None, None, None)
    albumSP = sp.album(albumID)
    if (albumTR[albumID] == '//'):

        songSP = sp.track(songID)
        songName = songSP['name']
        songDuration = songSP['duration_ms']
        song = Song(songName, songDuration, 0, 0)
        
        trackList.append(song)
        allSongs[songID] = song
    else:
        trackListSP = sp.album_tracks(albumID)
        print('         Tracks in this album:\n')
        for songSP in trackListSP['items']:    #creating a tracklist from the info retrieved from lastFM
            songName = songSP['name']
            songDuration = songSP['duration_ms']
            song = Song(songName, songDuration, 0, 0)
            trackList.append(song)
            print('             -->' + songName)
            allSongs[songSP['id']] = song
        print('\n')
        print('     Creating album object for \'' + str(albumTR[albumID]) + '\'')
        albumName = albumSP['name']
        albumReleaseDate = albumSP['release_date']
        album = Album(albumName, albumReleaseDate,  trackList, None, len(trackList), isFirstTimeListening)   #Creating an album object with all the tracks
        album.setDuration() #calculating the total duration of the album
    
    if (isTo == True and albumOrSong == 'S'):
        song = allSongs[songID]
        song.updateRepetitions(device, repetitions)
    else:
        print('         Im not updating \'PlayCount\' for this specific song: isTo = ' + str(isTo) + ', albumOrSong = ' + str(albumOrSong))

    if (isTo == True and albumOrSong == 'A'):
        album.updateRepetitions(device, repetitions)
    else:
        print('         Im not updating \'PlayCount\' for this specific album: isTo = ' + str(isTo) + ', albumOrSong = ' + str(albumOrSong))

    return (album, allSongs)