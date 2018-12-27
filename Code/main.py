"""Testing our classes"""

import csv
import logging

import load_review_functions as lrFN
from argparse import ArgumentParser

def setup():
    allArtists = {}
    allAlbums = {}
    allSongs = {}

    artistID = albumID = songID = None

    fieldnames = ['Date', 'Moment', 'ArtistFrom', 'AlbumFrom', 'SongFrom', 'ArtistTo', 'AlbumTo', 'SongTo', 'RootNode', 'AlbumSong', 'Repetitions', 'Device', 'isStreaming', 'isFirstListeningAlbum', 'Notes']

    parser = ArgumentParser()

    #parser.add_argument("-q", "--quiet", default=True, dest="quiet", help="Disable log")
    #parser.add_argument("-v", "--verbose", dest="verbose", help="Enable logging in stdout")
    #parser.add_argument("-vF", "--verboseFile", dest="verboseFile", help="Enable logging into logFile.log")

    parser.add_argument("-q", "--quiet", action='store_true', default=True, help="Disable log")
    parser.add_argument("-v", "--verbose", action='store_true', help="Enable logging in stdout")
    parser.add_argument("-vF", "--verboseFile", action='store_true', help="Enable logging into logFile.log")

    args = parser.parse_args()
    print(args)

    if (args.verbose == True):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    elif (args.verboseFile == True):
        logging.basicConfig(filename='./logFile.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    else:
        logging.disable(level=logging.INFO)
    
    '''
    args = parser.parse_args()
    print(args)

    rawLogLevel = 2 + (args.verbose or 0) - (args.quiet or 0)
    if rawLogLevel <= 0: 
        logLevel = logging.CRITICAL
    elif rawLogLevel == 1:
        logLevel = logging.ERROR
    elif rawLogLevel == 2:     # default
        logLevel = logging.WARNING
    elif rawLogLevel == 3: 
        logLevel = logging.INFO
    else:         
        logLevel = logging.DEBUG

    logging.basicConfig(level=logLevel, format='%(asctime)s - %(levelname)s - %(message)s')
    '''


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
            logging.info("--- BEGIN row: #" + str(i) + " ---")
            (artistID, albumID, songID) = lrFN.fileReview(row['ArtistFrom'], row['AlbumFrom'], row['SongFrom'], artistID, albumID, songID)
            lrFN.AASInfoLoading(artistID, albumID, songID, False, allArtists, allAlbums, allSongs, row['Device'], row['Repetitions'], row['AlbumSong'], row['isFirstListeningAlbum'])
            logging.info('\n')
            (artistID, albumID, songID) = lrFN.fileReview(row['ArtistTo'], row['AlbumTo'], row['SongTo'], artistID, albumID, songID)
            lrFN.AASInfoLoading(artistID, albumID, songID, True, allArtists, allAlbums, allSongs, row['Device'], row['Repetitions'], row['AlbumSong'], row['isFirstListeningAlbum'])
            logging.info('--- END ---\n')
            #writer.writerow(row)
            
        fileIN.close()
        #fileOUT.close()

def destroy():
    logging.info("Exiting application...")

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