"""Testing our classes"""

import functions_main as fn
import csv


allArtists = {}
allAlbums = {}
allSongs = {}
#Definisco il dizionario con tutti gli album
#Definisco il dizionario con tutti le canzoni

#leggo la linea, carico artista: se artista non è presente --> aggiungo --> non sarà presente nemmeno l'album --> aggiungo, -->aggiungo le canzoni dell'album aggiorno info --> next iteration
#se è presente, per quell'artista devo controllare album, se non è presente --> aggiungo, --> Aggiungo le canzoni e aggiorno info canzoni --> itero
#altrimenti per quell'album aggiorno le informazioni sulle canzoni (ripetizioni) --> itero

artist_el = ''
album_el = ''
song_el = ''
fieldnames = ['Date', 'Moment', 'ArtistFrom', 'AlbumFrom', 'SongFrom', 'ArtistTo', 'AlbumTo', 'SongTo', 'RootNode', 'AlbumSong', 'Repetitions', 'Device', 'isStreaming', 'isFirstListeningAlbum', 'Notes']

with open('/home/sem/OneDrive/Code/A_year_in_Music_2017_2018/Code/Musica.csv', 'r', newline='') as fileIN, open('/home/sem/OneDrive/Code/A_year_in_Music_2017_2018/Code/MusicaOUT.csv', 'w', newline='') as fileOUT:
    reader = csv.DictReader(fileIN, delimiter=',')
    writer = csv.DictWriter(fileOUT, fieldnames, extrasaction='ignore')
    writer.writeheader()
    i = 1
    for row in reader:
        i += 1
        print("Writing row: #" + str(i))
        (row['ArtistFrom'], row['AlbumFrom'], row['SongFrom']) = fn.fileReview(row['ArtistFrom'], row['AlbumFrom'], row['SongFrom'])
        fn.AASInfoGathering(row['ArtistFrom'], row['AlbumFrom'], row['SongFrom'], False, allArtists, allAlbums, allSongs, row['Device'], row['Repetitions'], row['AlbumSong'], row['isFirstListeningAlbum'])
        print('\n')
        (row['ArtistTo'], row['AlbumTo'], row['SongTo']) = fn.fileReview(row['ArtistTo'], row['AlbumTo'], row['SongTo'])
        fn.AASInfoGathering(row['ArtistTo'], row['AlbumTo'], row['SongTo'], True, allArtists, allAlbums, allSongs, row['Device'], row['Repetitions'], row['AlbumSong'], row['isFirstListeningAlbum'])
        print('---ITERATING---\n')
        writer.writerow(row)
        #Load on data structure
        
    fileIN.close()
    fileOUT.close()


'''
    for row in reader:
        i += 1
        #Lettura file IN, Scrittura file OUT con nomi corretti
        

        #Caricamento in memoria, lettura file OUT
        #(allArtists, allAlbums, allSongs) = fn.AASInfoGathering(row, writer, row['ArtistFrom'], row['AlbumFrom'], row['SongFrom'], False, allArtists, allAlbums, allSongs, row['Device'], row['Repetitions'], row['AlbumSong'], row['isFirstListeningAlbum'])
        fileIN.close()
        fileOUT.cloe()
        break
pass

        (allArtists, allAlbums, allSongs) = fn.AASInfoGathering(row, writer, row['ArtistTo'], row['AlbumTo'], row['SongTo'], True, allArtists, allAlbums, allSongs, row['Device'], row['Repetitions'], row['AlbumSong'], row['isFirstListeningAlbum'])
        print('---RIGA ' + str(i) + ' TERMINATA---')
'''

############################################################################################################################################################################


