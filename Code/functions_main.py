
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



def AASInfoGathering(artistName, albumName, songName, allArtists, allAlbums, allSongs, device, repetitions, albumOrSong):
    artistFM = network.get_artist(artistName)    
    artistName = artistFM.get_name(properly_capitalized=True)   #Returns the correct name of the artist

    albumFM = network.get_album(artistName, albumName)
    albumName = albumFM.get_name(properly_capitalized=True) #Returns the correct name of the album

    songFM = network.get_track(artistName, songName)
    songName = songFM.get_title(properly_capitalized=True)   #Returns the correct name of the song
    
    if (artistName in str(allArtists.keys())):
        print('     ' + artistName + " already added!")
        print('     Gathering \'' + albumName + '\' info...')
        if (albumName in str(allAlbums.keys())):
            print('     ' + albumName + ' already added!')
            print('     Gathering \'' + albumName + '\' info...')
            if (songName in str(allSongs.keys())):
                print('     ' + songName + ' already added!')
                print('     Updating \'' + songName + '\' info...')

                print('    --> DA FAREEEEE <--')
                #song = allSongs[songName]
                '''
                for song_el in allSongs:
                    if(song_el.getName() == song.getName()):
                        print('I\'ve found the song, updating info...')
                        break
                song_el.setDuration = songFM_From.get_duration                     ### PROBABLY SOME PROBLEMS HERE, HOW TO SELECT A SET ELEMENT AND MODIFY IT?
                if (row['Device'] == 'Smartphone'):
                    song_el.addSmartphonePlayCount(row['Repetitions'])
                elif (row['Device'] == 'Laptop'):
                    song_el.addLaptopPlayCount(row['Repetitions']) 
                else:
                    print('Song not found, adding it...')
                    allSongs.add(Song(song))
                    print('Song added, updating info...')
                    song.setDuration = songFM_From.get_duration
                    if (row['Device'] == 'Smartphone'):
                        song.addSmartphonePlayCount(row['Repetitions'])
                    elif (row['Device'] == 'Laptop'):
                        song.addLaptopPlayCount(row['Repetitions'])
                    print('Info updated!')
                    '''
            else:
                '''print('Album not found, collecting info and adding it...')
                album = Album(album)
                albumTracks = albumFM_From.get_tracks() #returns the list of tracks in this album
                for (el in albumTracks):
                    album.setTracks(el.get_name) #Adding tracks to the album
                    allSongs.add(Song(el.get_name)) #Adding song to the set of all songs
                print('Album and songs added, updating songs info...')
                for (el in album)


                album.setYear = albumFM_From.get_wiki_published_date() #Does it returns the publishing date of the album? --> CHECK
                album.setDuration() #knowing the list of all tracks in it, sums all the contained songs Durations and set the result as the album total duration
                #album.setNum_tracks() #Sets the total number of tracks contained in it
                '''       
    else:
        print(artistName + " not found in allArtists")
        print('     Creating an artist object for \'' + artistName + '\'')
            
        #Creating an artist object
        artist = Artist(artistName, artistFM.get_top_tags(limit=10), None, artistFM.get_similar(limit=20))

        print('     Creating a tracklist for \'' + artistName + '\'')
        print('     Updating \'allSongs\' collection...')
        trackList = []
        trackListFM = albumFM.get_tracks()

        for track_el in trackListFM:    #creating a tracklist from the info retrieved from lastFM
            track = Song(track_el.get_name(), track_el.get_duration())
            trackList.append(track)

        if(albumName == 'A'):
            for track_el in trackList:
                if (device == 'Smartphone'):
                    track_el.addSmartphonePlayCount(repetitions)
                elif (device == 'Laptop'):
                    track_el.addLaptopPlayCount(repetitions)
                    allSongs[track_el.getName()] = track_el
        elif (albumOrSong == 'S'):
            for track_el in trackList:
                if (track_el.getName() == track.getName()):
                    break
            if (device == 'Smartphone'):
                    track_el.addSmartphonePlayCount(int(repetitions))
            elif (device == 'Laptop'):
                track_el.addLaptopPlayCount(int(repetitions))
            allSongs[track_el.getName()] = track_el

        print('     Creating album object for \'' + albumName + '\'')
        album = Album(albumName, albumFM.get_wiki_published_date(), trackList)   #Creating an album object with all the tracks
        album.setDuration() #calculating the total duration of the album
        artist.addAlbums(album) #adding that album on the artist career
            
        print('     Updating \'allArtists\' collection...')
        allArtists[artistName] = artist
        print('     Updating \'allAlbums\' collection...')
        allAlbums[albumName] = album

        print('---ITERATING---')
        return (allArtists, allAlbums, allSongs);