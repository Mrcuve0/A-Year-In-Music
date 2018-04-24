
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

def albumCreation(artistName, albumName, songName, albumFM, songFM, allSongs, isTo, device, repetitions, albumOrSong, isFirstTimeListening):
    '''This function creates an album Object'''
    print('     Creating a tracklist for \'' + artistName + '\'')
    print('     Updating \'allSongs\' collection...')
    trackList = []
    if (albumName == '//'):
        track = Song(songFM.get_name(), songFM.get_duration())
        trackList.append(track)
    else:
        trackListFM = albumFM.get_tracks()
        print('         Tracks in this album:\n')
        for track_el in trackListFM:    #creating a tracklist from the info retrieved from lastFM
            track = Song(track_el.get_name(), track_el.get_duration())
            trackList.append(track)
            print('             -->' + track.getName())
        print('\n')

    if(albumOrSong == 'A'):
        for track_el in trackList:
            if (device == 'Smartphone' and isTo == True):
                track_el.addSmartphonePlayCount(repetitions)
            elif (device == 'Laptop' and isTo == True):
                track_el.addLaptopPlayCount(repetitions)
            allSongs[track_el.getName()] = track_el
    elif (albumOrSong == 'S'):
        for track_el in trackList:
            if (device == 'Smartphone' and isTo == True and track_el.getName() == songName):
                    track_el.addSmartphonePlayCount(int(repetitions))
            elif (device == 'Laptop'and isTo == True and track_el.getName() == songName):
                track_el.addLaptopPlayCount(int(repetitions))
            allSongs[track_el.getName()] = track_el
    else:
        print('         I\'m not updating \'PlayCount\': isTo = False')

    if (albumName != '//'):
        print('     Creating album object for \'' + albumName + '\'')
        album = Album(albumName, albumFM.get_wiki_published_date(), trackList, None, len(trackList), isFirstTimeListening)   #Creating an album object with all the tracks
        album.setDuration() #calculating the total duration of the album
    else:
        album = Album('//', None, None, None, None, None,)
    return (album, allSongs)
        


def AASInfoGathering(artistName, albumName, songName, isTo, allArtists, allAlbums, allSongs, device, repetitions, albumOrSong, isFirstTimeListening):
    '''This function loads all the data from the CSV file, entering new entries if none or updating them if already there'''
    artistFM = network.get_artist(artistName)    
    artistName = str(artistFM.get_name())   #Returns the correct name of the artist

    albumFM = network.get_album(artistName, albumName)
    if (albumName != '//'):
        albumName = str(albumFM.get_name()) #Returns the correct name of the album
    
    songFM = network.get_track(artistName, songName)
    songName = str(songFM.get_title(properly_capitalized=True))   #Returns the correct name of the song
    
    if (artistName in str(allArtists.keys())):
        print('     \'' + artistName + '\' already added!')
        print('     Gathering \'' + albumName + '\' info...')
        if (albumName in str(allAlbums.keys())):
            print('     \'' + albumName + '\' already added!')
            print('     Gathering \'' + albumName + '\' info...')
            if (songName in str(allSongs.keys())):
                print('     \'' + songName + '\' already added!')
                print('     Updating \'' + songName + '\' info...')
            else:
                print('         FATAL ERROR, SONG \'' + songName + '\' NOT FOUND!') #All the songs should already be in their respective albums
                return -1
            if (isTo == True):
                song_el = allSongs.get(songName)
                if (device == 'Smartphone'):
                    song_el.addSmartphonePlayCount(repetitions)
                elif (device == 'Laptop'):
                    song_el.addLaptopPlayCount(repetitions)
            else:
                print('         I\'m not updating \'PlayCount\': isTo = False')
        else:   #Album not found
            print('         Album \'' + albumName + '\' not found, collecting info and adding it...')
            artist = Artist(artistName, artistFM.get_top_tags(limit=10), None, artistFM.get_similar(limit=20))
            (album, allSongs) = albumCreation(artistName, albumName, songName, albumFM, songFM, allSongs, isTo, device, repetitions, albumOrSong, isFirstTimeListening)
            artist.addAlbums(album) #adding that album on the artist career
    else:
        print('\''+ artistName + '\' not found in allArtists')
        print('     Creating an artist object for \'' + artistName + '\'')
            
        #Creating an artist object
        artist = Artist(artistName, artistFM.get_top_tags(limit=10), None, artistFM.get_similar(limit=20))
        (album, allSongs) = albumCreation(artistName, albumName, songName, albumFM, songFM, allSongs, isTo, device, repetitions, albumOrSong, isFirstTimeListening)

        artist.addAlbums(album) #adding that album on the artist career
            
        print('     Updating \'allArtists\' collection...')
        allArtists[artistName] = artist
        print('     Updating \'allAlbums\' collection...')
        allAlbums[albumName] = album

    print('---ITERATING---\n')
    return (allArtists, allAlbums, allSongs);