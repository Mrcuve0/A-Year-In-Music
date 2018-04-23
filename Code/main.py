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

i = 0
with open('Musica.csv', 'r') as file:
    reader = csv.DictReader(file, delimiter=',')
    for row in reader:
        i += 1
        (allArtists, allAlbums, allSongs) = fn.AASInfoGathering(row['ArtistFrom'], row['AlbumFrom'], row['SongFrom'], False, allArtists, allAlbums, allSongs, row['Device'], row['Repetitions'], row['AlbumSong'])
        (allArtists, allAlbums, allSongs) = fn.AASInfoGathering(row['ArtistTo'], row['AlbumTo'], row['SongTo'], True, allArtists, allAlbums, allSongs, row['Device'], row['Repetitions'], row['AlbumSong'])
        print('finito')


############################################################################################################################################################################


