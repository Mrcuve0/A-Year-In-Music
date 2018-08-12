import os
import spotipy
import json
from fuzzywuzzy import process
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')

client_credentials_mng = SpotifyClientCredentials(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_mng)

#Search an artist
artist = sp.search(q='todd terje', type='artist')
artistName = artist['artists']['items'][0]['name']
artistID = artist['artists']['items'][0]['id']
artistPopularity = artist['artists']['items'][0]['popularity']
artistFollowers = artist['artists']['items'][0]['followers']['total']
print(artistName) #print Artist's name
print(artistID) #print Artist's ID
print(artistPopularity)

print('\'' + artistName + '\' genres: ')
for genre in artist['artists']['items'][0]['genres']:
    print(genre)

#Search an album
album = sp.search(q='Alive 2007', type='album')
albumName = album['albums']['items'][0]['name']
albumReleaseDate = album['albums']['items'][0]['release_date']
albumID = album['albums']['items'][0]['id']
albumType = album['albums']['items'][0]['album_type']
trackList = sp.album_tracks(albumID)
print(albumName)
print(albumReleaseDate)
print(albumID)
print(albumType)
print(trackList)

#Search a track
track = sp.search(q='Robot Rock / Oh Yeah', type='track')
trackName = track['tracks']['items'][0]['name']
trackID = track['tracks']['items'][0]['id']
trackNumber = track['tracks']['items'][0]['track_number']
trackPopularity = track['tracks']['items'][0]['popularity']
trackIsExplicit = track['tracks']['items'][0]['explicit']
trackDuration = track['tracks']['items'][0]['duration_ms']
trackInAlbumID = track['tracks']['items'][0]['album']['id']

#Given the ArtistID, find the related song (given a songName, there could be more related artists and even more related albums)
artist = sp.search(q='muse', type='artist')
artistID = artist['artists']['items'][0]['id']

'''
album = sp.search(q='the 2nd law', type='album', limit=20)
for i in range(0, len(album['albums']['items'])):
    if (str(album['albums']['items'][int(i)]['artists'][0]['id']) == str(artistID)):
        albumName = album['albums']['items'][0]['name']
        albumID = album['albums']['items'][0]['id']
        break

track = sp.search(q='muse the 2nd law animals', type='track', limit=20)
for i in range(0, len(track['tracks']['items'])):
    if (track['tracks']['items'][i]['album']['id'] == albumID and track['tracks']['items'][i]['album']['artists'][0]['id'] == artistID):
        trackName = track['tracks']['items'][i]['name']
        break
'''
artistName = 'Todd Terje'
artistSP = sp.search(q='artist:\"' + artistName + '\"', type='artist')
artists_list = []
for i in range(0, artistSP['artists']['total']):
    artists_list.append(artistSP['artists']['items'][i]['name'])
result = process.extractOne(artistName, artists_list)
index = artists_list.index(result[0])
artistName = artistSP['artists']['items'][index]['name']
artistID = artistSP['artists']['items'][index]['id'] 