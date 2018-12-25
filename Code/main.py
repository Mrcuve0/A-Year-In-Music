"""Testing our classes"""

import csv
import load_review_functions as lrFN

def setup():
    allArtists = {}
    allAlbums = {}
    allSongs = {}

    artistID = albumID = songID = None

    fieldnames = ['Date', 'Moment', 'ArtistFrom', 'AlbumFrom', 'SongFrom', 'ArtistTo', 'AlbumTo', 'SongTo', 'RootNode', 'AlbumSong', 'Repetitions', 'Device', 'isStreaming', 'isFirstListeningAlbum', 'Notes']
    return (allArtists, allAlbums, allSongs, artistID, albumID, songID, fieldnames)


def loadFromFile(allArtists, allAlbums, allSongs, artistID, albumID, songID, fieldname):
    with open('/home/sem/OneDrive/Code/A_year_in_Music_2017_2018/Code/Musica_(2017_2018).csv', 'r', newline='') as fileIN:
        #, open('/home/sem/OneDrive/Code/A_year_in_Music_2017_2018/Code/MusicaMusica_(2017_2018)_OUT.csv', 'w', newline='') as fileOUT:
        reader = csv.DictReader(fileIN, delimiter=',')
        #writer = csv.DictWriter(fileOUT, fieldnames, extrasaction='ignore')
        #writer.writeheader()
        i = 1
        for row in reader:
            i += 1
            print("Writing row: #" + str(i))
            (artistID, albumID, songID) = lrFN.fileReview(row['ArtistFrom'], row['AlbumFrom'], row['SongFrom'], artistID, albumID, songID)
            lrFN.AASInfoLoading(artistID, albumID, songID, False, allArtists, allAlbums, allSongs, row['Device'], row['Repetitions'], row['AlbumSong'], row['isFirstListeningAlbum'])
            print('\n')
            (artistID, albumID, songID) = lrFN.fileReview(row['ArtistTo'], row['AlbumTo'], row['SongTo'], artistID, albumID, songID)
            lrFN.AASInfoLoading(artistID, albumID, songID, True, allArtists, allAlbums, allSongs, row['Device'], row['Repetitions'], row['AlbumSong'], row['isFirstListeningAlbum'])
            print('---ITERATING---\n')
            #writer.writerow(row)
            
        fileIN.close()
        #fileOUT.close()

def destroy():
    print("Exiting application...")

def listeningTimeArtist(artistName, artistID):
    pass

def listeningTimeAlbum(albumName, albumID):
    pass

def listeningTimeSong(songName, songID):
    pass

if __name__ == '__main__':
        (allArtists, allAlbums, allSongs, artistID, albumID, songID, fieldname) = setup()
        loadFromFile(allArtists, allAlbums, allSongs, artistID, albumID, songID, fieldname)

        #for loop that iterates on the artists
            #listeningTimeArtist(artistName, artistID)

        #for loop that iterates on the albums

        #for loop that iterates on the songs