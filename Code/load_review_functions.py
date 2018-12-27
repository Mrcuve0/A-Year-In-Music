
from artist_class import Artist
from album_class import Album
from song_class import Song 

import os
import sys
from dotenv import load_dotenv, find_dotenv
from fuzzywuzzy import process
import logging

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

load_dotenv(find_dotenv())
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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

def nameMatching(objectSP, objectName, prevObjectID, category):
    '''Using FuzzyWuzzy library: given a list of possible artist/album/song names, let's find the one we're lookin for, using approximate string matching.
    returns: (artist/album/song)Name, (artist/album/song)ID
    '''
    # I want to look for the song that is in the albumName that I already found! I want to avoid to look in the wrong album, I'll otain a different ID!
    # This happen, for instance, when different version of an album exist ("Deluxe/anniversary/Cover" albums)
    object_list = []
    if objectSP[category]['total'] > objectSP[category]['limit']:
        max_range = 'limit'
    else:
        max_range = 'total'

    found = 0
    if (objectSP[category][max_range] != 0):
        for i in range(0, objectSP[category][max_range]):
            if category == 'albums':
                for j in range(0, len(objectSP[category]['items'][i]['artists'])):
                    if (objectSP[category]['items'][i]['artists'][j]['id'] == prevObjectID):
                        object_list.append(objectSP[category]['items'][i]['name'])
                        found = i
                    else:
                        object_list.append('//')
            elif category == 'tracks':
                if (objectSP[category]['items'][i]['album']['id'] == prevObjectID):
                    object_list.append(objectSP[category]['items'][i]['name'])
                    found = i
                else:
                    object_list.append('//')
            else:
                object_list.append(objectSP[category]['items'][i]['name'])
        result = process.extractOne(objectName, object_list)
        index = object_list.index(result[0])
        if (category != 'artists' and len(objectSP[category]['items'][found]['artists']) > objectSP[category][max_range]):
            index = found
        objectName = objectSP[category]['items'][index]['name'] #Saving the fixed artist/album/song name
        objectID = objectSP[category]['items'][index]['id'] #saving the fixed artist/album/song ID
    else:
        logging.info("FATAL ERROR! No elements found in \'"+ category + "\' category, \'" + objectName + "\' not found.")
    

    return (objectName, objectID)

def spotifyExceptionHandling(e):
    '''Spotify exception handling: network errors (401, 204, 404, 502) are handled here'''
    logging.info('---Exception raised!---')
    if (str(e.http_status) == str(401)):    #Unauthorized
        logging.info('The request requires user authentication or, if the request included authorization credentials, authorization has been refused for those credentials.')
        sys.exit(e.msg)
    if (str(e.http_status) == str(204)):    #No Content
        logging.info('The request has succeeded but returns no message body.')
        sys.exit(e.msg)
    elif (str(e.http_status) == str(404)):    #Not Found
        logging.info('The requested resource could not be found. This error can be due to a temporary or permanent condition.')
        sys.exit(e.msg)
    elif (str(e.http_status) == str(502)):    #Bad Gateway
        logging.info('The server was acting as a gateway or proxy and received an invalid response from the upstream server.')
        sys.exit(e.msg)
    else:
        logging.info('Exception error: ' + str(e.http_status) + ', ' + str(e.msg))

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
                (artistName, artistID) = nameMatching(artistSP, artistName, None, 'artists')   #approximate string matching (in: list of artist names, out: the most similar artistName matching our CSV entry)

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

    logging.info('artistName: ' + artistName + ', ID: ' + artistID)
        
    if (albumNameOLD in albumConv.keys()) :  #AlbumName already processed and fixed
        albumName = albumConv.get(albumNameOLD) #retrieving the correct name
        albumID = album_ID_dict.get(albumName)  #retrieving the correct ID
    elif (albumNameOLD in albumConv.values()):
        pass
    else:   #the album hasn't been already processed, let's find its correct name spelling and its ID
        try:

            '''
            elif (str(albumName).lower() == str('Dope').lower()):
                albumID = '7zPgCo3kXvezF86DQw2ERZ' 
            '''
            
            if (str(albumName).lower() == str('Rage Against The Machine').lower()): #Exceptions manually added
                albumID = '4LaRYkT4oy47wEuQgkLBul'
            elif (str(albumName).lower() == str('Dream Sequence').lower()):
                albumID = '7ALFR4o9ZXfqNVv9EOORn1'
            elif (str(albumName).lower() == str('while(1<2)').lower()):
                albumID = '7iDqcnIHjisPl2Yf4hsf8f'
            elif (str(albumName).lower() == str('Until One').lower()):
                albumID = '5JRoPXvkRBmwyAA2fkMWgY'
            elif (str(albumName).lower() == str('Glamour').lower()):
                albumID = '1O8xo7V5Jo326PbctFBVdj'
            elif (str(albumName).lower() == str('My Salsoul').lower()):     #TIP: If the artist/album/song is not present in spotify's DB, let the ID point to a dummy artist/album/song
                albumID = '//'
            elif (str(albumName).lower() == str('Sacrebleu').lower()):
                albumID = '//'
            elif (str(albumName).lower() == str('Leftovers EP').lower()):
                albumID = '//'
            elif (str(albumName).lower() == str('//').lower()):
                albumID = '//'
            else:
                #albumSP = sp.search(q=str('\"' + artistName + '\" \"' + albumName + '\" NOT ' + 'Anniversary'), type='album')   #Looking for the album in Spotify's DB
                #albumSP = sp.search(q=str(artistName + ' ' + albumName + ' NOT ' + 'Anniversary'), type='album', limit=30)   #Looking for the album in Spotify's DB
                albumSP = sp.search(q=str(artistName + ' ' + albumName), type='album', limit=20)   #Looking for the album in Spotify's DB
                if (albumName != '//' and albumSP['albums']['total'] != 0):     
                    (albumName, albumID) = nameMatching(albumSP, albumName, artistID, 'albums')   #approximate string matching         
                    
                elif (albumSP['albums']['total'] == 0):
                    sys.exit('FATAL ALBUM ERROR! \'' + albumName + '\' Not Found! Exiting...') #ERROR

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

    logging.info('albumName: ' + albumName + ', ID: ' + albumID)
    
    if (songNameOLD in songConv.keys()):    #SongName already processed and fixed
        songName = songConv.get(songNameOLD)    #retrieving the correct name
        songID = song_ID_dict.get(songName)     #retrieving the correct ID
    elif (songNameOLD in songConv.values()):
        pass
    else:   #the song hasn't been already processed, let's find its correct name spelling and its ID
        try:

            '''
            elif (str(songName).lower() == str('Dope - Original Mix').lower()):
                songID = '5wElWRFQIzeE1YBe1gTIxp'
                   
            elif (str(songName).lower() == str('Leave the World Behind').lower()):
                songID = '3ueNIaHaq1EvW6OOzfGXz7'          
            
            elif(str(songName).lower() == str('Until One').lower()):
                songID = '2vU6kbZI3bLM6ASsnSe11J'    
            elif(str(songName).lower() == str('I\'m Losing More Than I\'ll ever Have').lower()):
                songID = '3jEJQGprFXpeICSRtPKGDc'
            elif(str(songName).lower() == str('She\'s Thunderstorms').lower()):
                songID = '5xw2cHVLw1rlDPp3cL9Zuv'
            '''

            if (str(songName).lower() == str('Bombtrack').lower()):   #Exceptions manually added
                songID = '6ZU9RJIZ0fNaFuQM57bDIA'
            elif (str(songName).lower() == str('Killing in the Name').lower()):   #Exceptions manually added
                songID = '3FUS56gKr9mVBmzvlnodlh'
            elif (str(songName).lower() == str('Take the Power Back').lower()):   #Exceptions manually added
                songID = '3tTL7jlSkowXidYeafFtwG'
            elif (str(songName).lower() == str('Settle for Nothing').lower()):   #Exceptions manually added
                songID = '2vuDdXqekkDCSdawJyUpT6'
            elif (str(songName).lower() == str('Bulllet In the Head').lower()):   #Exceptions manually added
                songID = '11cxKUEgnVAlesUKt4e3br'
            elif (str(songName).lower() == str('Know Your Enemy').lower()):   #Exceptions manually added
                songID = '1IDAJagxB9AQjjYXaiDK1j'
            elif (str(songName).lower() == str('Wake Up').lower()):   #Exceptions manually added
                songID = '6zbHSDJjgrNdfIxPyGfPBt'
            elif (str(songName).lower() == str('Fistful of Steel').lower()):   #Exceptions manually added
                songID = '3YEk8mVdMI7rxtfimlUd1G'
            elif (str(songName).lower() == str('Township Rebellion').lower()):   #Exceptions manually added
                songID = '0WK0EqiidP6WEDOHK34HEe'
            elif (str(songName).lower() == str('Freedom').lower()):   #Exceptions manually added
                songID = '1zVE9JBBy8j0KmlbM8Xwhi'
            elif (str(songName).lower() == str('The Dream Is Always The Same').lower()):
                songID = '5iRVl2TQ54sk9KMed2iUDy' 
            elif(str(songName).lower() == str('Love On A Real Train').lower()):
                songID = '49y78l709VxMkIcq7jUJKN'
            elif(str(songName).lower() == str('Bloodflood pt. II').lower()):
                songID = '60AEGzxRNUQ3Pzg4tygzJC'
            elif(str(songName).lower() == str('Introduzione').lower()):
                songID = '4pgWywTML1NToZ17quJusD'
            elif (str(songName).lower() == str('71c').lower()):
                songID = '//'
            elif (str(songName).lower() == str('The Magnificent').lower()):
                songID = '//'
            elif (str(songName).lower() == str('Hyperlandia').lower()):
                songID = '//'
            elif(str(songName).lower() == str('San Salvador').lower()):
                songID = '//'
            elif (str(songName).lower() == str('Seconds').lower()):
                songID = '//'
            elif (str(songName).lower() == str('Prologue').lower()):
                songID = '//'
            else:
                #songSP = sp.search(q=str('artist:' + artistName + ' album:' + albumName + ' track:' + songName), type='track')  #Looking for the song in Spotify's DB
                #songSP = sp.search(q=str('artist:' + artistName + 'track:' + songName), type='track', limit=50)  
                #songSP = sp.search(q=str('\"' + artistName + '\" \"' + songName), type='track', limit=50) 
                #songSP = sp.search(q=str(artistName + ' ' + songName), type='track', limit=20) 
                songSP = sp.search(q=str(artistName + ' ' + songName), limit=20) 
                #Looking for the song in Spotify's DB
                (songName, songID) = nameMatching(songSP, songName, albumID, 'tracks')   #approximate string matching  

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

    logging.info('songName: ' + songName + ', ID: ' + songID)
    return (artistID, albumID, songID)

def AASInfoLoading(artistID, albumID, songID, isTo, allArtists, allAlbums, allSongs, device, repetitions, albumOrSong, isFirstTimeListening):
    '''Core function that loads all the data from the CSV file, entering new entries (artist, Album or Song) if none or updating them if already there.
    returns: allArtists, allAlbums, allSongs'''

    if (artistID == '//'):
        return
    if (albumID == '//'):
        return
    if (songID == '//'):
        return


    if (artistID in allArtists.keys()): #Artist already loaded in program memory
        logging.info('     Artist \'' + str(ID_artist_dict[artistID]) + '\' already added!')
        logging.info('     Gathering Album \'' + str(ID_album_dict[albumID]) + '\' info...')
        if (albumID in allAlbums.keys()):   #album already added in program memory
            logging.info('     Album \'' + str(ID_album_dict[albumID]) + '\' already added!')
            logging.info('     Gathering Song \'' + str(ID_song_dict[songID]) + '\' info...')
            if (songID in allSongs.keys()): #song already added in program memory
                logging.info('     Song \'' + str(ID_song_dict[songID]) + '\' already added!')
                logging.info('     Updating Song \'' + str(ID_song_dict[songID]) + '\' info...')

                if (isTo == True and albumOrSong == 'S'):
                    song = allSongs[songID]
                    song.updateRepetitions(device, repetitions) #Updating repetitions for this specific song
                else:
                    logging.info('         Im not updating \'PlayCount\' for this specific song: isTo = ' + str(isTo) + ', albumOrSong = ' + str(albumOrSong))

            else:   #ERROR
                logging.info('         FATAL ERROR, SONG \'' + ID_song_dict[songID] + '\' NOT FOUND!') #All the songs should already be in their respective albums
                pass
            if (isTo == True and albumOrSong == 'A'):
                album = allAlbums[albumID]
                album.updateRepetitions(device, repetitions)    #Updating repetitions for the whole tracklist of the album
            else:
                logging.info('         Im not updating \'PlayCount\' for this specific album: isTo = ' + str(isTo) + ', albumOrSong = ' + str(albumOrSong))
        else:   #Album not found
            logging.info('         Album \'' + ID_album_dict[albumID] + '\' not found, collecting info and adding it...')
            artist = allArtists[artistID]
            (album, allSongs) = albumCreation(artistID, albumID, songID, songSP, allAlbums, allSongs, isTo, device, repetitions, albumOrSong, isFirstTimeListening)
            artist.addAlbums(album) #adding that album on the artist career
            allAlbums[albumID] = album
    else:
        logging.info('Artist \''+ str(ID_artist_dict[artistID]) + '\' not found in allArtists')
        logging.info('     Creating an artist object for \'' + str(ID_artist_dict[artistID]) + '\'')
            
        #Creating an artist object
        artistSP = sp.artist(artistID)
        artist = Artist(artistSP['id'], artistSP['name'], artistSP['followers']['total'], artistSP['genres'], None, artistSP['popularity'], sp.artist_related_artists(artistID))
        (album, allSongs) = albumCreation(artistID, albumID, songID, songSP, allAlbums, allSongs, isTo, device, repetitions, albumOrSong, isFirstTimeListening)

        artist.addAlbums(album) #adding that album on the artist career 
        logging.info('     Updating \'allArtists\' collection...')
        allArtists[artistID] = artist    
        logging.info('     Updating \'allAlbums\' collection...')
        allAlbums[albumID] = album
    return (allArtists, allAlbums, allSongs)

def albumCreation(artistID, albumID, songID, songSP, allAlbums, allSongs, isTo, device, repetitions, albumOrSong, isFirstTimeListening):
    '''This function creates an album Object, looks (on Discogs) for the tracklist and then updates Song details (duration, date, Number of repetitions etc...)
    returns: album, AllSongs'''

    logging.info('     Creating a tracklist for \'' + str(ID_album_dict[albumID]) + '\'')
    logging.info('     Updating \'allSongs\' collection...')

    trackList = []
    album = Album(None, None, None, None, None, None)
    
    if (ID_album_dict[albumID] == '//'):

        songSP = sp.track(songID)
        song = Song(songSP['id'], songSP['name'], songSP['duration_ms'], 0, 0)
        
        trackList.append(song)
        allSongs[songID] = song
    else:
        albumSP = sp.album(albumID)
        trackListSP = sp.album_tracks(albumID)
        logging.info('         Tracks in this album:\n')
        for songSP in trackListSP['items']:    #creating a tracklist from the info retrieved from spotify
            song = Song(songSP['id'], songSP['name'], songSP['duration_ms'], 0, 0)
            trackList.append(song)
            logging.info('             -->' + songSP['name'])
            allSongs[songSP['id']] = song
        logging.info('\n')
        logging.info('     Creating album object for \'' + str(ID_album_dict[albumID]) + '\'')        
        album = Album(albumSP['id'], albumSP['name'], albumSP['release_date'], albumSP['release_date_precision'], albumSP['label'],  albumSP['popularity'], trackList, None, len(trackList), isFirstTimeListening)   #Creating an album object with all the tracks
        album.setDuration() #calculating the total duration of the album
    
    if (isTo == True and albumOrSong == 'S'):
        song = allSongs[songID]
        song.updateRepetitions(device, repetitions)
    else:
        logging.info('         Im not updating \'PlayCount\' for this specific song: isTo = ' + str(isTo) + ', albumOrSong = ' + str(albumOrSong))

    if (isTo == True and albumOrSong == 'A'):
        album.updateRepetitions(device, repetitions)
    else:
        logging.info('         Im not updating \'PlayCount\' for this specific album: isTo = ' + str(isTo) + ', albumOrSong = ' + str(albumOrSong))

    return (album, allSongs)