
from artist_class import Artist
from album_class import Album
from song_class import Song 

import os
import sys
from dotenv import load_dotenv, find_dotenv
from fuzzywuzzy import process

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

load_dotenv(find_dotenv())

######## SPOTIFY ########
client_credentials_mng = SpotifyClientCredentials(os.getenv('SPOTIFY_CLIENT_ID'), os.getenv('SPOTIFY_CLIENT_SECRET'))
sp = spotipy.Spotify(client_credentials_manager=client_credentials_mng)
spE = spotipy.SpotifyException

artistConv = {} 
albumConv = {}
songConv = {}

ID_artist_dict = {} #k: ID, value: artistName
ID_album_dict = {}  #k: ID, value: albumName
ID_song_dict  = {}  #k: ID, value: songName

artist_ID_dict = {} #k: artistName, value: ID
album_ID_dict = {}  #k: albumName, value: ID
song_ID_dict = {}   #k: songName, value: ID

artistSP = None #Spotify artist object
albumSP = None  #Spotify album object
songSP = None   #Spotify song object

def nameMatching(objectSP, objectName, category):
    '''Using FuzzyWuzzy library: given a list of possible artist/album/song names, let's find the one we're lookin for, using approximate string matching.
    returns: (artist/album/song)Name, (artist/aolbum/song)ID
    '''
    object_list = []
    if objectSP[category]['total'] > objectSP[category]['limit']:
        max_range = 'limit'
    else:
        max_range = 'total'
    for i in range(0, objectSP[category][max_range]):
        object_list.append(objectSP[category]['items'][i]['name'])

    result = process.extractOne(objectName, object_list)    #We're assuming the name with the highest score is the one we're looking for
    index = object_list.index(result[0])

    objectName = objectSP[category]['items'][index]['name'] #Saving the fixed artist/album/song name
    objectID = objectSP[category]['items'][index]['id'] #saving the fixed artist/album/song ID

    return (objectName, objectID)

def spotifyExceptionHandling(e):
    '''Spotify exception handling: network errors (401, 204, 404, 502) are handled here'''
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

def fileReview(artistName, albumName, songName, artistID, albumID, songID):
    '''Reviews the input file, looks (on Spotify) for the correct spelling of artistName, albumName and songName.
    Retrieves artistID, albumID and songID.
    In order to avoid too many requests to Spotify server, everytime a name conversion is completed, it's added in a dict, '.*Conv'
    so the next time I'll find the wrong spelling I can look for it in the dict instead of repeating the network request.
    returns: artistID, albumID, songID
    '''
    artistNameOLD = artistName
    albumNameOLD = albumName
    songNameOLD = songName
    
    if (artistNameOLD in artistConv.keys()):    #ArtistName already processed and fixed
        artistName = artistConv.get(artistNameOLD)  #retrieving the correct name
        artistID = artist_ID_dict.get(artistName)   #retrieving the artistID

    elif (artistNameOLD in artistConv.values()):
        pass
    else:   #the artist hasn't been already processed, let's find its correct name spelling and its ID
        try:
            if (str(artistName).lower() == str('Butch').lower()):   #Butch is an exception manually added
                artistID = str('5kLzaeSHrmS7okc5XNE6lv')
            else:
                artistSP = sp.search(q='artist:\"' + artistName + '\"', type='artist')  #Looking for the artist in Spotify's DB
                (artistName, artistID) = nameMatching(artistSP, artistName, 'artists')   #approximate string matching (in: list of artist names, out: the most similar artistName matching our CSV entry)

        except TypeError:
            sys.exit('\'' + artistName + '\' Not Found! TypeError, exiting...') #ERROR
        except IndexError:
            sys.exit('\'' + artistName + '\' Not Found! IndexError, exiting...')    #ERROR 
        except spE as e: 
            spotifyExceptionHandling(e)
            sys.exit('\'' + artistNameOLD + '\' not found in Spotify library, exiting...')  #ERROR

        artistConv[artistNameOLD] = artistName  #Updating dicts
        ID_artist_dict[artistID] = artistName
        artist_ID_dict[artistName] = artistID

    print('artistName: ' + artistName + ', ID: ' + artistID)
        
    if (albumNameOLD in albumConv.keys()) :  #AlbumName already processed and fixed
        albumName = albumConv.get(albumNameOLD) #retrieving the correct name
        albumID = album_ID_dict.get(albumName)  #retrieving the correct ID
    elif (albumNameOLD in albumConv.values()):
        pass
    else:   #the album hasn't been already processed, let's find its correct name spelling and its ID
        try:
            if (str(albumName).lower() == str('Rage Against The Machine').lower()): #Exceptions manually added
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
                albumSP = sp.search(q=str('\"' + artistName + '\" \"' + albumName + '\" NOT ' + 'Anniversary'), type='album')   #Looking for the album in Spotify's DB
                if (albumName != '//' and albumSP['albums']['total'] != 0):     
                    (albumName, albumID) = nameMatching(albumSP, albumName, 'albums')   #approximate string matching         
                    
                elif (albumSP['albums']['total'] == 0):
                    sys.exit('\'' + albumName + '\' Not Found! Exiting...') #ERROR

        except TypeError:
            sys.exit('\'' + albumName + '\' Not Found! TypeError, exiting...')  #ERROR           
        except IndexError:
            sys.exit('\'' + albumName + '\' Not Found! IndexError, exiting...') #ERROR  
        except spE as e: 
            spotifyExceptionHandling(e)
            sys.exit('\'' + albumNameOLD + '\' not found in Spotify library, exiting...')   #ERROR
            
        albumConv[albumNameOLD] = albumName #Updating dicts
        ID_album_dict[albumID] = albumName
        album_ID_dict[albumName] = albumID

    print('albumName: ' + albumName + ', ID: ' + albumID)
    
    if (songNameOLD in songConv.keys()):    #SongName already processed and fixed
        songName = songConv.get(songNameOLD)    #retrieving the correct name
        songID = song_ID_dict.get(songName)     #retrieving the correct ID
    elif (songNameOLD in songConv.values()):
        pass
    else:   #the song hasn't been already processed, let's find its correct name spelling and its ID
        try:
            if (str(songName).lower() == str('Killing in the Name').lower()):   #Exceptions manually added
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
            elif (str(songName).lower() == str('71c').lower()):
                songID = '71c'
            elif(str(songName).lower() == str('Love On A Real Train').lower()):
                songID = '49y78l709VxMkIcq7jUJKN'
            elif(str(songName).lower() == str('Until One').lower()):
                songID = '2vU6kbZI3bLM6ASsnSe11J'    
            else:
                songSP = sp.search(q=str('artist:' + artistName + ' album:' + albumName + ' track:' + songName), type='track')  #Looking for the song in Spotify's DB
                (songName, songID) = nameMatching(songSP, songName, 'tracks')   #approximate string matching  

        except TypeError:
            sys.exit('\'' + songName + '\' Not Found! TypeError, exiting...')   #ERROR   
        except IndexError:
            sys.exit('\'' + songName + '\' Not Found! IndexError, exiting...')  #ERROR  
        except spE as e: 
            spotifyExceptionHandling(e)
            sys.exit('\'' + songNameOLD + '\' not found in Spotify library, exiting...')    #ERROR
           
        songConv[songNameOLD] = songName    #Updating dicts
        ID_song_dict[songID] = songName
        song_ID_dict[songName] = songID

    print('songName: ' + songName + ', ID: ' + songID)
    return (artistID, albumID, songID)

def AASInfoLoading(artistID, albumID, songID, isTo, allArtists, allAlbums, allSongs, device, repetitions, albumOrSong, isFirstTimeListening):
    '''Core function that loads all the data from the CSV file, entering new entries (artist, Album or Song) if none or updating them if already there.
    returns: allArtists, allAlbums, allSongs'''
    
    '''
    artistFM = network.get_artist(artistName)    
    albumFM = network.get_album(artistName, albumName)
    songFM = network.get_track(artistName, songName)
    '''

    if (artistID == '5Il27M5JXuQLgwDgVrQMgo'):   #Dimitri from Paris, artist with no sufficient infos on Spotifys
        return
    if (songID == '71c'):
        return


    if (artistID in allArtists.keys()): #Artist already loaded in program memory
        print('     Artist \'' + str(ID_artist_dict[artistID]) + '\' already added!')
        print('     Gathering Album \'' + str(ID_album_dict[albumID]) + '\' info...')
        if (albumID in allAlbums.keys()):   #album already added in program memory
            print('     Album \'' + str(ID_album_dict[albumID]) + '\' already added!')
            print('     Gathering Song \'' + str(ID_song_dict[songID]) + '\' info...')
            if (songID in allSongs.keys()): #song already added in program memory
                print('     Song \'' + str(ID_song_dict[songID]) + '\' already added!')
                print('     Updating Song \'' + str(ID_song_dict[songID]) + '\' info...')

                if (isTo == True and albumOrSong == 'S'):
                    song = allSongs[songID]
                    song.updateRepetitions(device, repetitions) #Updating repetitions for this specific song
                else:
                    print('         Im not updating \'PlayCount\' for this specific song: isTo = ' + str(isTo) + ', albumOrSong = ' + str(albumOrSong))

            else:   #ERROR
                print('         FATAL ERROR, SONG \'' + ID_song_dict[songID] + '\' NOT FOUND!') #All the songs should already be in their respective albums
                pass
            if (isTo == True and albumOrSong == 'A'):
                album = allAlbums[albumID]
                album.updateRepetitions(device, repetitions)    #Updating repetitions for the whole tracklist of the album
            else:
                print('         Im not updating \'PlayCount\' for this specific album: isTo = ' + str(isTo) + ', albumOrSong = ' + str(albumOrSong))
        else:   #Album not found
            print('         Album \'' + ID_album_dict[albumID] + '\' not found, collecting info and adding it...')
            artist = allArtists[artistID]
            (album, allSongs) = albumCreation(artistID, albumID, songID, songSP, allAlbums, allSongs, isTo, device, repetitions, albumOrSong, isFirstTimeListening)
            artist.addAlbums(album) #adding that album on the artist career
            allAlbums[albumID] = album
    else:
        print('Artist \''+ str(ID_artist_dict[artistID]) + '\' not found in allArtists')
        print('     Creating an artist object for \'' + str(ID_artist_dict[artistID]) + '\'')
            
        #Creating an artist object
        artistSP = sp.artist(artistID)
        artist = Artist(artistSP['name'], artistSP['genres'], None, sp.artist_related_artists(artistID))
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

    print('     Creating a tracklist for \'' + str(ID_album_dict[albumID]) + '\'')
    print('     Updating \'allSongs\' collection...')

    trackList = []
    album = Album(None, None, None, None, None, None)
    
    if (ID_album_dict[albumID] == '//'):

        songSP = sp.track(songID)
        songName = songSP['name']
        songDuration = songSP['duration_ms']
        song = Song(songName, songDuration, 0, 0)
        
        trackList.append(song)
        allSongs[songID] = song
    else:
        albumSP = sp.album(albumID)
        trackListSP = sp.album_tracks(albumID)
        print('         Tracks in this album:\n')
        for songSP in trackListSP['items']:    #creating a tracklist from the info retrieved from spotify
            songName = songSP['name']
            songDuration = songSP['duration_ms']
            song = Song(songName, songDuration, 0, 0)
            trackList.append(song)
            print('             -->' + songName)
            allSongs[songSP['id']] = song
        print('\n')
        print('     Creating album object for \'' + str(ID_album_dict[albumID]) + '\'')
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