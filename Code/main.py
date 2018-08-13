"""Testing our classes"""

import csv
import load_review_functions as lrFN


allArtists = {}
allAlbums = {}
allSongs = {}

artistID = albumID = songID = None

fieldnames = ['Date', 'Moment', 'ArtistFrom', 'AlbumFrom', 'SongFrom', 'ArtistTo', 'AlbumTo', 'SongTo', 'RootNode', 'AlbumSong', 'Repetitions', 'Device', 'isStreaming', 'isFirstListeningAlbum', 'Notes']

with open('/home/sem/OneDrive/Code/A_year_in_Music_2017_2018/Code/Musica.csv', 'r', newline='') as fileIN:
    #, open('/home/sem/OneDrive/Code/A_year_in_Music_2017_2018/Code/MusicaOUT.csv', 'w', newline='') as fileOUT:
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

############################################################################################################################################################################